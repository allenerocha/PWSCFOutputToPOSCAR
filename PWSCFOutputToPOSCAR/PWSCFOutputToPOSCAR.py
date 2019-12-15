#!/usr/bin/env python3
"""This module parses through the file and makes calls to the atom module and other utilities"""

import sys
import utils.parse_data
import utils.lattice_parameter
import utils.lattice_vectors
import utils.atomic_positions


def main():
    """Main method"""

    def display_help() -> None:
        """
        Displays the README.md file
        :return: None
        """
        with open('../README.md', 'r') as help_file:
            for line in help_file.readlines():
                print(line.rstrip())

    def check_file(input_file: str) -> None:
        """
        Checks if the input file is valid
        :param input_file: path of the file
        :return: None
        """
        if '.out' not in input_file_path and '.unfinished' not in input_file_path:
            raise TypeError(
                'Invalid file type! Expected a *.out, received a *.{}.\nUse -h for help.'.format(
                    input_file.split(".")[-1]))

    input_file_path = ''
    file_format = ''
    if sys.argv[1] == '-help' or sys.argv[1] == 'help' or sys.argv[1] == 'h':
        display_help()
        sys.exit()

    # read from standard input mode
    if sys.argv[1] == '-stdin':
        input_file_path = '{}.{}.{}.out'.format(sys.argv[2], sys.argv[3], sys.argv[4])
        with open(input_file_path, 'w') as data_file:
            if not sys.stdin.isatty():
                lines = sys.stdin
                for line in lines:
                    data_file.write(line)

    else:
        # file to be parsed (including path)
        input_file_path = sys.argv[1]

    # call to check the inputted file
    check_file(input_file_path)

    # assigns both the file type and format
    file_type = input_file_path.split('.')[-1]

    for word in input_file_path.split('.'):
        if word in ['vc-relax', 'scf']:
            file_format = word

    # if the user does not wish to change the directory
    output_file_path = ''

    # the user wants to save the file in a new directory
    if len(sys.argv) == 3 or len(sys.argv) == 6:
        # sets the output file path to a new location
        output_file_path = sys.argv[len(sys.argv) - 1]

    # parses the file based on the type and format of the file
    lines = utils.parse_data.parse_file(file_type, file_format, input_file_path)
    # lines = parse_file(file_type, file_format, input_file_path)
    if sys.argv[1] == '-stdin':
        file_name = '{}.{}.'.format(sys.argv[2], sys.argv[3])
    else:
        file_name = ''.join(str(e + '.') for e in input_file_path.split('/')[-1].split('.')[0:2])
    write_file(lines, file_name, file_format, file_type, input_file_path, output_file_path)


def write_file(lines, file_name, file_format, file_type, input_file_path, output_file_path):
    # opens/creates output file to write
    """
    Args:
        lines: lines of the input data
        file_name: name of the file to be written to
        file_format: format of the input data
        file_type: extension of the data
        input_file_path: path of the input data
        output_file_path: location to save the POSCAR.VASP file
    """
    with open('{}{}POSCAR.VASP'.format(output_file_path, file_name), 'w') as out_file:

        # writes the first line [Symbols] [Symmetry group]
        out_file.write(''.
                       join(str(e + ' ') for e in input_file_path.split('/')[-1].split('.')[0:2]))

        out_file.write('\n')
        # three spaces for the current line
        out_file.write('   ')
        # element 9 will be the line with the lattice parameter
        # regex to remove all non-numerical characters except the "."
        out_file.write(utils.lattice_parameter.get_lattice_parameter(lines, file_format))
        out_file.write('\n')

        lattice_vectors = utils.lattice_vectors.get_lattice_vectors(lines, file_format)

        # write the lattice vectors to file
        for index, lattice_vector in enumerate(lattice_vectors):
            # case 1: first component is negative
            if lattice_vectors[0] == '-' and index == (0, 3, 6):
                out_file.write('    {}'.format(lattice_vector))

            # case 2: first component is not negative
            elif lattice_vector[0] != '-' and index in (0, 3, 6):
                out_file.write('     {}'.format(lattice_vector))

            # case 3: non-first component is negative
            elif lattice_vector[0] == '-' and index not in (0, 3, 6):
                out_file.write('   {}'.format(lattice_vector))

            # case 3: non-first component is not negative
            elif lattice_vector[0] != '-' and index not in (0, 3, 6):
                out_file.write('    {}'.format(lattice_vector))

            # new line after the last component in the vector
            if index in (2, 5, 8):
                out_file.write('\n')

        elements = utils.atomic_positions.get_atomic_positions(lines, file_type, file_format)

        out_file.write('   ')
        # rows for elements and length
        for row in range(2):
            # columns
            for element in elements:
                # first row (symbols)
                if row == 0:
                    out_file.write(element.get_symbol())
                    out_file.write('   ')
                # second row (amount of vectors)
                else:
                    out_file.write(str(element.size()))
                    out_file.write('  ')

            out_file.write('\n')
            if row != 1:
                out_file.write('     ')

        out_file.write('Direct')
        out_file.write('\n')

        for element in elements:
            # rows
            for row in range(element.size()):
                # case 1: first component is negative
                if element.get_x_pos(row)[0] == '-':
                    out_file.write('     {}'.format(element.get_x_pos(row)))

                # case 2: first component is not negative
                if element.get_x_pos(row)[0] != '-':
                    out_file.write('      {}'.format(element.get_x_pos(row)))

                # case 3: second component is negative
                if element.get_y_pos(row)[0] == '-':
                    out_file.write('  {}'.format(element.get_y_pos(row)))

                # case 4: second component is not negative
                if element.get_y_pos(row)[0] != '-':
                    out_file.write('   {}'.format(element.get_y_pos(row)))

                # case 5: third component is negative
                if element.get_z_pos(row)[0] == '-':
                    out_file.write('  {}'.format(element.get_z_pos(row)))
                    out_file.write('\n')

                # case 6: third component is not negative
                if element.get_z_pos(row)[0] != '-':
                    out_file.write('   {}'.format(element.get_z_pos(row)))
                    out_file.write('\n')
        out_file.write('\n')
        total_elements = 0

        # get total amount of elements
        for index, element in enumerate(elements):
            total_elements += element.size()
            if index == (len(elements) - 1):
                for _ in range(total_elements):
                    out_file.write('  0.00000000E+00  0.00000000E+00  0.00000000E+00')
                    out_file.write('\n')


if __name__ == '__main__':
    main()
