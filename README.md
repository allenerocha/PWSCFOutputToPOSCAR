# PWSCFOutputToPOSCAR
Python script (command line executable) to take Quantum ESPRESSO pw.x vc-relax output (example: Si.Fd-3m.vc-relax.out) and generate VASP POSCAR file named [element].[symmetry group].POSCAR.VASP in file format below, converting vc-relax output alat from Bohr to Angstrom (multiply by 0.529177)

POSCAR File Format

=================

(chemical formula)          (Hermann-Mauguin notation for symmetry group)

(lattice parameter)

(a11) (a12) (a13)

(a21) (a22) (a23)                               [lattice vectors]

(a31) (a32) (a33)

(chemical element symbol 1) (chemical element symbol 2) …

(number of type 1 atoms) (number of type 2 atoms) …

Direct                                                    [atom coordinates in terms of lattice vectors]

                (atom 1 x coordinate) (atom 1 y coordinate) (atom 1 z coordinate)

                (atom 2 x coordinate) (atom 2 y coordinate) (atom 2 z coordinate)

               …

 

[zeros]

 

=================
