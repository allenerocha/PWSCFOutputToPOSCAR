# PWSCFOutputToPOSCAR

./PWSCFOutputToPOSCAR.py [ARGUMENT] [OPTION 1] [OPTION 2] [OPTION 3] [OPTION 4]

    [ARGUMENT]                          [DESCRIPTION]
    -stdin                              read from standard input and output the .out & .vasp files
        [OPTION 1]                      chemical formula
        [OPTION 2]                      symmetry group
        [OPTION 3]                      file format
        [OPTION 4]                      output path (empty for the same directory)
        
    -f                                  read from file
        [OPTION 1]                      full filepath of input file
        [OPTION 2]                      file output path with trailing '/' 
                                        (empty for filepath of input file)
                                        
    help -help -h                       display this file in the terminal
        
      
# Examples / Usage:

    Reading from standard input
        Output the .out file and the .POSCAR.VASP file to the relative directory 'output_files'.
        ./PWSCFOutputToPOSCAR.py -stdin Si Fd-3m scf output_files/

        Output the .out file and the .POSCAR.VASP file to the current path.
        ./PWSCFOutputToPOSCAR.py -stdin Si Fd-3m scf
        
    Reading from input file
        Read from input file 'Si.Fd-3m.scf.out' located in the relative directory 'input_files' and save the .VASP output to the relative directory 'output_files'.
        ./PWSCFOutputToPOSCAR.py -f input_files/Si.Fd-3m.scf.out output_files/

        Read from input file 'Si.Fd-3m.scf.out' located in the relative directory 'input_files' and save the .VASP output to the current path.
        ./PWSCFOutputToPOSCAR.py -f input_files/Si.Fd-3m.vc-relax.out


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

contact allenerocha@pm.me for any questions or inquires
