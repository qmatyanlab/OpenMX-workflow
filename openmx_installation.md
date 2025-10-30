# OpenMX on Ubuntu

Installation test on DFTWS4. The main issue is the compiler. Intel remove the support of the classic `icc` `ifort` . The installation gets more trickier as we need an 2023 version of intel compiler. Luckily someone test and found a stable way to install OpenMX based on the new 2025 oneAPI toolkit. [https://sites.google.com/site/ytl821/home/codes](https://sites.google.com/site/ytl821/home/codes)

With the new oneAPI and HPC toolkit from Intel:

Load the environment first

```python
source /opt/intel/oneapi/setvars.sh
```

check the compilers (LLVM set)

```python
which icx icpx ifx
icx  --version
ifx  --version
```

with the output:

```python
/opt/intel/oneapi/compiler/2025.2/bin/icx
/opt/intel/oneapi/compiler/2025.2/bin/icpx
/opt/intel/oneapi/compiler/2025.2/bin/ifx
Intel(R) oneAPI DPC++/C++ Compiler 2025.2.1 (2025.2.0.20250806)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/intel/oneapi/compiler/2025.2/bin/compiler
Configuration file: /opt/intel/oneapi/compiler/2025.2/bin/compiler/../icx.cfg
ifx (IFX) 2025.2.1 20250806
Copyright (C) 1985-2025 Intel Corporation. All rights reserved.
```

check if the MPI present

```python
which mpirun mpiicx mpiifx
echo "$I_MPI_ROOT"
test -d "$I_MPI_ROOT/include" && echo "MPI headers OK"
```

with the output:

```python
/opt/intel/oneapi/mpi/2021.16/bin/mpirun
/opt/intel/oneapi/mpi/2021.16/bin/mpiicx
/opt/intel/oneapi/mpi/2021.16/bin/mpiifx
/opt/intel/oneapi/mpi/2021.16
MPI headers OK
```

check if the MKL is present 

```python
echo "$MKLROOT"
test -d "$MKLROOT/include" && echo "MKL headers OK"
test -d "$MKLROOT/lib/intel64" && echo "MKL libs OK"
```

with the output:

```python
/opt/intel/oneapi/mkl/2025.2
MKL headers OK
MKL libs OK
```

modified the `makefile` located in the `source/` folder

```python
MKLROOT    = /opt/intel/oneapi/mkl/2025.2
CC = mpiicx -O3 -xHOST -fiopenmp -fcommon -Wno-error=implicit-function-declaration -I${MKLROOT}/include -I${MKLROOT}/include/fftw
FC = mpiifx -O3 -xHOST -fiopenmp
LIB= -L${MKLROOT}/lib/intel64 -lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -lifcore -lmkl_blacs_intelmpi_lp64 -liomp5 -lpthread -lm -ldl
```

and execute the following 

```python
make clean
make all
```

installation should be done around few minutes.

Go to work directory and test the installation:

```python
cd ../work
mpirun -np 1 ./openmx -runtest
```

and should see the following:

```python
cat runtest.result
   1  input_example/Benzene.dat        Elapsed time(s)=   11.46  diff Utot= 0.000000000029  diff Force= 0.000000000001
   2  input_example/C60.dat            Elapsed time(s)=   79.51  diff Utot= 0.000000000007  diff Force= 0.000000000005
   3  input_example/CO.dat             Elapsed time(s)=   16.95  diff Utot= 0.000000000026  diff Force= 0.000000008290
   4  input_example/Cr2.dat            Elapsed time(s)=   12.62  diff Utot= 0.000000000025  diff Force= 0.000000000075
   5  input_example/Crys-MnO.dat       Elapsed time(s)=   56.21  diff Utot= 0.000000000012  diff Force= 0.000000000056
   6  input_example/GaAs.dat           Elapsed time(s)=   81.01  diff Utot= 0.000000000006  diff Force= 0.000000000001
   7  input_example/Glycine.dat        Elapsed time(s)=   18.09  diff Utot= 0.000000000001  diff Force= 0.000000000001
   8  input_example/Graphite4.dat      Elapsed time(s)=    8.30  diff Utot= 0.000000000014  diff Force= 0.000000000053
   9  input_example/H2O-EF.dat         Elapsed time(s)=   10.37  diff Utot= 0.000000000001  diff Force= 0.000000000003
  10  input_example/H2O.dat            Elapsed time(s)=    8.08  diff Utot= 0.000000000001  diff Force= 0.000000003207
  11  input_example/HMn.dat            Elapsed time(s)=   27.85  diff Utot= 0.000000000131  diff Force= 0.000000000021
  12  input_example/Methane.dat        Elapsed time(s)=    7.00  diff Utot= 0.000000000003  diff Force= 0.000000000001
  13  input_example/Mol_MnO.dat        Elapsed time(s)=   17.24  diff Utot= 0.000000000187  diff Force= 0.000000000148
  14  input_example/Ndia2.dat          Elapsed time(s)=    8.57  diff Utot= 0.000000000001  diff Force= 0.000000000000

Total elapsed time (s)      363.27
```

and if you do 

```python
mpirun -np 8 ./openmx -runtest
cat runtest.result
   1  input_example/Benzene.dat        Elapsed time(s)=    4.82  diff Utot= 0.000000000038  diff Force= 0.000000000004
   2  input_example/C60.dat            Elapsed time(s)=   17.59  diff Utot= 0.000000000004  diff Force= 0.000000000001
   3  input_example/CO.dat             Elapsed time(s)=    8.85  diff Utot= 0.000000000096  diff Force= 0.000000000238
   4  input_example/Cr2.dat            Elapsed time(s)=    9.84  diff Utot= 0.000000000912  diff Force= 0.000000000172
   5  input_example/Crys-MnO.dat       Elapsed time(s)=   22.61  diff Utot= 0.000000000011  diff Force= 0.000000000003
   6  input_example/GaAs.dat           Elapsed time(s)=   38.07  diff Utot= 0.000000000004  diff Force= 0.000000000001
   7  input_example/Glycine.dat        Elapsed time(s)=    5.36  diff Utot= 0.000000000001  diff Force= 0.000000000001
   8  input_example/Graphite4.dat      Elapsed time(s)=    5.97  diff Utot= 0.000000000022  diff Force= 0.000000000012
   9  input_example/H2O-EF.dat         Elapsed time(s)=    5.20  diff Utot= 0.000000000000  diff Force= 0.000000000001
  10  input_example/H2O.dat            Elapsed time(s)=    4.81  diff Utot= 0.000000000000  diff Force= 0.000000000512
  11  input_example/HMn.dat            Elapsed time(s)=   13.68  diff Utot= 0.000000000132  diff Force= 0.000000000002
  12  input_example/Methane.dat        Elapsed time(s)=    3.91  diff Utot= 0.000000000004  diff Force= 0.000000000001
  13  input_example/Mol_MnO.dat        Elapsed time(s)=    9.74  diff Utot= 0.000000000371  diff Force= 0.000000000011
  14  input_example/Ndia2.dat          Elapsed time(s)=    7.55  diff Utot= 0.000000000001  diff Force= 0.000000000000

Total elapsed time (s)      157.98
```
