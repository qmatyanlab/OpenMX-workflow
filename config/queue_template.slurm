#!/bin/bash -l

#SBATCH -A project_number
#SBATCH --output=%J.out
#SBATCH --error=%J.error
#SBATCH -N 1
#SBATCH -C cpu
#SBATCH -q premium
#SBATCH -J openmx_wf
#SBATCH -t 02:00:00

ssh -Nf -L 12347:localhost:27017 db0host # example of how to link your mongoDB. This is now mount on the computation node with port = 12347

export PATH="$PATH:/path/to/your/openmx/source"

# If you're using NERSC, the following might be your compiler, if not, please change it to the compiler you use when doing the OpenMX calculations.
module load PrgEnv-intel
module load intel-classic/2023.2.0
module load cray-fftw
module load conda 

conda activate /path/to/atomate_env

$${pre_rocket}
cd $${launch_dir}
$${rocket_launch}
$${post_rocket}

# CommonAdapter (SLURM) completed writing Template
