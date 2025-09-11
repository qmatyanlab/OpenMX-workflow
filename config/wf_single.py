from atomate.openmx.fireworks.core import OpenmxScfFW
from atomate.openmx.powerups import add_additional_fields_to_taskdocs, set_execution_options

from pymatgen.core.structure import Structure  # fixed: import from core
from pymatgen.io.vasp.inputs import Kpoints
from fireworks import LaunchPad
from fireworks import Workflow

from monty.serialization import loadfn
import pandas as pd

class GetStructure:
    def __init__(self, file):
        # Read only the first entry from the JSON file
        data = loadfn(file)
        self.df = pd.DataFrame({
            "material_id": [data["material_id"][0]],
            "structure": [data["structure"][0]],
            "point_group": [data["point_group"][0]],
        })

    def get_sts(self):
        return [(row['material_id'], row['structure'], row['point_group']) for _, row in self.df.iterrows()]


class SingleRunner:
    def __init__(self, launchpad_file, json_file):
        self.lpad = LaunchPad.from_file(launchpad_file)
        self.getsts = GetStructure(json_file)

    def run_one(self, kppa=2000):
        st_dict = self.getsts.get_sts()
        mpid, structure, pg= st_dict[0]

        print(f"Running single structure: {mpid}")

        fw = OpenmxScfFW(
            structure=structure,
            run_deeph_preprocess=True,
            run_permittivity=True,
            run_shift_current=True, 
            override_default_openmx_params={"kppa": kppa, "scf_criterion": 3.67e-8}
        )
        wf = Workflow([fw], name=f"{mpid}")

        def get_kpts(kppa, structure):
            kpoints = Kpoints.automatic_density(structure, kppa)
            for i in range(3):
                if kpoints.kpts[0][i] % 2 == 0:
                    kpoints.kpts[0][i] += 1
            print("KPOINTS:", kpoints.kpts)
            return kpoints

        get_kpts(kppa, structure)

        wf = add_additional_fields_to_taskdocs(wf, {"mp-id": mpid, "category": "sc_testing_wf", "pointgroup": pg})
        wf = set_execution_options(wf, category="sc_testing_wf")

        self.lpad.add_wf(wf)
        print("Workflow added to LaunchPad.")


if __name__ == "__main__":
    runner = SingleRunner(
        "/path/to/your/my_launchpad.yaml",
        "/path/to/your/filtered_structures_with_metadata.json"
    )
    runner.run_one()
