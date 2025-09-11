# OpenMX Workflow

A high-throughput workflow for **OpenMX** calculations using [atomate](https://github.com/hackingmaterials/atomate).

This repository is primarily adapted from [openmx-wf](https://github.com/tsaie79/openmx-wf) by [@tsaie79](https://github.com/tsaie79).  
The main extension is the post-processing of OpenMX outputs (`.scfout` and `.out`) to compute response functions such as:

- Frequency-dependent **permittivity**
- **Shift current conductivity**
- Other related **optical response tensors**

---

## Prerequisites

This workflow assumes that users:

- Are familiar with **OpenMX** and have a compiled version installed.
- Have **Julia** installed
- Have the packages required by [DeepH](https://github.com/mzjb/DeepH-pack)  
  (only [HopTB.jl](https://github.com/HopTB/HopTB.jl) needs to be added in addition).
- Have access to a running **MongoDB** instance for job and data management.

---
