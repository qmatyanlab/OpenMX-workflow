# OpenMX Workflow

A high-throughput workflow for **OpenMX** calculations using [atomate](https://github.com/hackingmaterials/atomate). 
This workflow was also employed in our recent work: [arXiv:2505.04862](https://arxiv.org/abs/2505.04862).

This repository is adapted from [openmx-wf](https://github.com/tsaie79/openmx-wf) by [@tsaie79](https://github.com/tsaie79).  
The main extension is the post-processing of OpenMX outputs (`.scfout` and `.out`) to compute response functions such as:

- Frequency-dependent **permittivity** tensor
- **Shift current conductivity** tensor

---

## Prerequisites

This workflow assumes that users:

- Are familiar with **OpenMX** and have a compiled version **3.9** installed.
- Have **Julia** installed.
- Have the packages required by [DeepH](https://github.com/mzjb/DeepH-pack).  
  (Additionally, you will need [HopTB.jl](https://github.com/HopTB/HopTB.jl).)
- Have access to a running **MongoDB** instance for job and data management.

---

## Installation

To set up the environment, run:

```bash
pip install -r requirements.txt
```
This will install the necessary dependencies for the workflow, including two custom packages:

- **pymatgen** (custom fork) – provides a custom-defined basis set for passing into the `ASE.Atoms` object.  
- **atomate** (custom fork) – enables job submission and data storage.

---

## Usage

1. Configure your workflow using the provided configuration files.  
   See [openmx-wf](https://github.com/tsaie79/openmx-wf) and the [atomate documentation](https://atomate.org/) for details.

2. Once configured, run:

   ```bash
   python config/wf_poscar_direct.py
   ```
This will:

- Convert your input into the required `openmx.dat` format.  
- Insert the workflow into the FireWorks database (MongoDB).

From your designated launch site, execute the workflow using FireWorks:

```bash
qlaunch singleshot
```
or
```bash
qlaunch rapidfire -m 1
```
## Citing

If you use this workflow in your research, please cite:

```
@misc{hsu2025accuratepredictionsequentialtensor,
      title={Accurate Prediction of Tensorial Spectra Using Equivariant Graph Neural Network}, 
      author={Ting-Wei Hsu and Zhenyao Fang and Arun Bansil and Qimin Yan},
      year={2025},
      eprint={2505.04862},
      archivePrefix={arXiv},
      primaryClass={cond-mat.mtrl-sci},
      url={https://arxiv.org/abs/2505.04862}, 
}
```

