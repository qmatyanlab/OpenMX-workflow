from typing import Optional

from fireworks import LaunchPad, Workflow
from pymatgen.core import Structure
from atomate.openmx.fireworks.core import OpenmxScfFW
from atomate.openmx.powerups import add_additional_fields_to_taskdocs, set_execution_options
def submit_single_openmx_from_poscar(
    launchpad_file: str,
    poscar_path: str = "./POSCAR",
    name: str = "single_openmx_scf",
    kppa: int = 2000,
    scf_criterion: float = 3.67e-08,
    run_deeph_preprocess: bool = True,
    run_permittivity: bool = False,
    run_shift_current: bool = False,
    category: Optional[str] = None,
    extra_fields: Optional[dict] = None,
):
    """Read a POSCAR and submit a single OpenMX SCF FW to LaunchPad."""
    # 1) Connect LP
    lpad = LaunchPad.from_file(launchpad_file)

    # 2) Read structure
    structure = Structure.from_file(poscar_path)

    # 3) Build FW (minimal args)
    fw = OpenmxScfFW(
        structure=structure,
        run_deeph_preprocess=run_deeph_preprocess,
        run_permittivity = run_permittivity,
        run_shift_current = run_shift_current,
        override_default_openmx_params={"kppa": kppa, "scf_criterion": scf_criterion},
        name=name,
    )

    # 4) (Optional) attach metadata / category
    wf = Workflow([fw], name=name)
    # if extra_fields:
    #     wf = add_additional_fields_to_taskdocs(wf, extra_fields)
    # if category:
    wf = set_execution_options(wf, category=category)

    # 5) Submit
    lpad.add_wf(wf)
    return True

submit_single_openmx_from_poscar(
    launchpad_file="/path/to/your/config/my_launchpad.yaml",
    poscar_path="/path/to/your/POSCAR",
    name="test_single_SCF",
    kppa=2000,
    scf_criterion=3.67e-08,
    run_deeph_preprocess=True,
    run_permittivity = True,
    category=">>this need to match with my_fworker.yaml<<",           
    # extra_fields={"source": "local_poscar"}  # optional
)
