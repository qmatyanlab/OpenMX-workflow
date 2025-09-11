using HopTB
using DelimitedFiles
using StaticArrays
using HDF5
using LinearAlgebra

@everywhere function extract_chemical_potential_from_scfout(scfout_path)
    # Open the SCFOUT file
    openmx_file = open(scfout_path, "r")
    
    # Read the file line by line
    for line in eachline(openmx_file)
        # Look for the line containing "Chemical potential" or a similar keyword
        if occursin(r"Chemical potential \(Hartree\)", line)
            # Extract the chemical potential value from the line
            # Assuming the chemical potential is the last number on the line
            chemical_potential = parse(Float64, split(line)[end])
            close(openmx_file)
            return chemical_potential
        end
    end
    
    # If no chemical potential line is found, return an error message
    close(openmx_file)
    throw("Chemical potential not found in SCFOUT file.")
end

Hartree2ev = 27.2114
pattern = r".*\.scfout$"  # Regex to match *.vasp.run
files = filter(f -> occursin(pattern, f), readdir("."))
isempty(files) && error("No .scfout file found in current directory!")
println(files)
scfout_path = files[1]
tm = HopTB.Interface.createmodelopenmx(scfout_path)
println(tm.norbits)
μ = extract_chemical_potential_from_scfout(scfout_path) * Hartree2ev 
println(μ)
sm = SharedTBModel(tm)
kgrid_density = 0.025  # in units of 1/Å
# Compute mesh size
meshsize = [round(Int, norm(tm.rlat[i, :]) / kgrid_density) for i in 1:3]
meshsize = [x % 2 == 0 ? x : x + 1 for x in meshsize]  
println("Calculated mesh size: ", meshsize)

ωs = collect(range(0.0, stop=20, length=2001))
num_ωs = length(ωs)
gauss_width = 0.05

# Allocate real-only tensor: (α, β, γ, ω)
tensor = zeros(Float64, 3, 3, 3, num_ωs)

for α in 1:3
    for β in 1:3
        for γ in β:3  # only compute when γ ≥ β to enforce symmetry
            println("Calculating for α = $α, β = $β, γ = $γ")

            sc = HopTB.Optics.get_shift_cond(sm, α, β, γ, ωs, μ, meshsize, ϵ=gauss_width, batchsize=8)

            # Assign σ_{αβγ}
            tensor[α, β, γ, :] .= real(sc)

            # Enforce σ_{αβγ} = σ_{αγβ}
            if β != γ
                tensor[α, γ, β, :] .= real(sc)
            end
        end
    end
end

# Save to file
filename = "sc_tensor_kgd_$(kgrid_density).dat"
open(filename, "w") do f
    write(f, "# k grid density: $kgrid_density\n")
    write(f, "# kmesh: $(meshsize[1])x$(meshsize[2])x$(meshsize[3])\n")
    write(f, "# epsilon (gauss_width): $gauss_width\n")
    write(f, "# fermi_level: $μ\n")
    write(f, "# Columns: ω, σ_111, σ_112, ..., σ_333 (real only)\n\n")

    for i in 1:num_ωs
        row = [ωs[i]]
        for α in 1:3, β in 1:3, γ in 1:3
            push!(row, tensor[α, β, γ, i])
        end
        writedlm(f, [row], " ")
    end
end

println("Shift current tensor (real) written to $filename")
