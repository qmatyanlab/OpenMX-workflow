## Workflow Scripts

1. **`wf_batch.py`**  
   Handles **batch processing**.  
   Users provide a `.json` file containing all the structures for high-throughput calculations.  
   Recommended fields include the **structure**, **formula**, and **mp_id**.

2. **`wf_poscar_direct.py`**  
   Designed for quick **single-shot submissions** to test the workflow.  
   Takes a `POSCAR` file (e.g., downloaded from the Materials Project) directly as input.

3. **`wf_single.py`**  
   Handles **single processing** for testing.  
   Similar to `wf_batch.py`, but can work with a large `.json` file containing thousands of structures, while still allowing single-shot execution for debugging or validation.

4. **Important note**  
   Users should carefully check the **smearing** and **k-grid density** parameters in  
   - `calc_permittivity.jl`  
   - `calc_shift_current.jl`  
   to ensure they are appropriate for their calculations.
