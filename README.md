# PWSCFOutputToPOSCAR
Python script (command line executable) to take Quantum ESPRESSO pw.x vc-relax output (example: Si.Fd-3m.vc-relax.out) and generate VASP POSCAR file named [element].[symmetry group].POSCAR.VASP in file format below, converting vc-relax output alat from Bohr to Angstrom (multiply by 0.529177)
