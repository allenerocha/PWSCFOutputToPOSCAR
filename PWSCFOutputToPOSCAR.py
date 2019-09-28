#!/usr/bin/python
# Version 3.0
# Changes:
#   Added standard input functionality

from sys import argv, stdin
import re


def main():
    class atom:
        def __init__(self, symbol, x_pos, y_pos, z_pos):
            self.symbol = symbol
            self.x_pos = []
            self.x_pos.append(x_pos)
            self.y_pos = []
            self.y_pos.append(y_pos)
            self.z_pos = []
            self.z_pos.append(z_pos)
            self.length = 0

        def get_symbol(self):
            return self.symbol

        def add_vector(self, x_pos, y_pos, z_pos):
            self.x_pos.append(x_pos)
            self.y_pos.append(y_pos)
            self.z_pos.append(z_pos)
            self.length += 1

        def get_x_pos(self, i):
            return self.x_pos[i]

        def get_y_pos(self, i):
            return self.y_pos[i]

        def get_z_pos(self, i):
            return self.z_pos[i]

        def increase_length(self):
            self.length += 1

        def leng(self):
            return self.length

    def display_help():
        with open('README.md','r') as help_file:
            for line in help_file.readlines():
                print(line.rstrip())

    def check_file(input_file=''):
        if '.out' not in input_file_path and '.unfinished' not in input_file_path:
            print('Invalid file type.')
            print('Expected a *.out, received a *.{}.'.format(input_file.split('.')[-1]))
            display_help()
            exit()

    def parse_file(file_type='', file_format='', input_file_path=''):
        lines = []
        # vcf format
        # tries to open
        try:
            with open('{}'.format(input_file_path), 'r') as in_file:
                # upper bound of the text to save
                upper_bound = 0
                # upper bound has been found
                upper_bound_flag = False
                # lower bound of the text to parse
                lower_bound = 0
                if file_type == 'out' and file_format == 'vc-relax':
                    # iterates through the file adding each of the lines to the list
                    for line in in_file:
                        # adds the current line of the string to the list
                        lines.append(line.strip())
                        # checks if the upper bound flag has been tripped
                        if upper_bound_flag is False:
                            # increments until the upper bound flag is tripped
                            upper_bound += 1
                        # checks if the current line is the flag
                        if line.strip() == 'Final estimate of lattice vectors (input alat units)':
                            # trips the upper bound flag
                            upper_bound_flag = True
                        # checks for lower bound
                        if line.strip() == 'End final coordinates':
                            # lower bound found, breaks out of the code to save some time
                            break
                        # increment the lower bound integer
                        lower_bound += 1
                    # removes unnecessary elements from the list
                    lines = lines[upper_bound:lower_bound]

                # scf format
                elif file_type == 'out' and file_format == 'scf':
                    # iterates through the file adding each of the lines to the list
                    for line in in_file:
                        # adds the current line of the string to the list
                        lines.append(line.strip())
                        # checks if the upper bound flag has been tripped
                        if upper_bound_flag is False:
                            # increments until the upper bound flag is tripped
                            upper_bound += 1
                        # checks if the current line is the flag
                        if 'bravais-lattice index' in line.strip():
                            # trips the upper bound flag
                            upper_bound_flag = True
                        # checks for lower bound
                        if 'number of k points' in line.strip():
                            # lower bound found, breaks out of the code to save some time
                            break
                        # increment the lower bound integer
                        lower_bound += 1
                    # removes unnecessary elements from the list
                    lines = lines[upper_bound:lower_bound]

                # unfinished file
                else:
                    # iterates through the file adding each of the lines to the list
                    for line in in_file:
                        # adds the current line of the string to the list
                        lines.append(line.strip())
                        # checks if the upper bound flag has been tripped
                        if upper_bound_flag is False:
                            # increments until the upper bound flag is tripped
                            upper_bound += 1
                        # checks if the current line is the flag
                        if 'new lattice vectors (alat unit)' in line.strip():
                            # trips the upper bound flag
                            upper_bound_flag = True
                        # checks for lower bound
                        if 'Writing output data file' in line.strip():
                            # lower bound found, breaks out of the code to save some time
                            break
                        # increment the lower bound integer
                        lower_bound += 1
                    # removes unnecessary elements from the list
                    lines = lines[upper_bound:lower_bound]
            return lines

        # input file does not exist
        except FileNotFoundError as e:
            print(str(e))
            exit()

    # uses a regex to search for the line:
    # CELL_PARAMETERS (alat= [NUMBER])                  <-*.vc-relax.*
    # or
    # lattice parameter (alat)  =      [NUMBER]  a.u    <-*.scf.*
    # depending on the file type format
    def get_lattice_parameter(lines=[], file_format=''):
        # input file was in vc-relax format
        regex = re.compile(r'[^0-9.]')
        lattice_parameter = ''
        if file_format == 'vc-relax':
            for line in lines:
                if 'CELL_PARAMETERS' in line.strip():
                    lattice_parameter = str(float(regex.sub('', line)) * 0.529177)

        # input file was in scf format
        else:
            for line in lines:
                if 'lattice parameter' in line.strip():
                    # [lattice][parameter][alat][=][10.3618][a.u.]
                    lattice_parameter = str(float(re.sub(r'\s+', ' ', line).split(' ')[4]) * 0.529177)
        return lattice_parameter

    # iterates through the list of lines looking for the lattice vectors:
    # uses a regex to look for the lattice vectors depending on the file type format
    # next line after:
    # new lattice vectors (alat unit) :                         <*.out.unfinished
    # or
    # Final estimate of lattice vectors (input alat units)      <*.out
    # next line after:
    def get_lattice_vectors(lines=[], file_type='', file_format=''):
        lattice_vectors = []
        # input file was in vc-relax format
        if file_format == 'vc-relax':
            index = 0
            lattice_flag = False
            # add the sublist of lattice vectors from the
            # first three elements of the lines list
            for line in lines:
                if 'unit-cell' in line:
                    break
                for w in line.split(' '):
                    if w != '':
                        lattice_vectors.append(w)

        # input file was in scf format
        else:
            index = 0
            lattice_flag = False
            for line in lines:
                if lattice_flag:
                    for w in line.split(' '):
                        if not w.isalpha() and '.' in w:
                            lattice_vectors.append(w)
                    index += 1
                if index > 2:
                    break
                if 'crystal axes:' in line:
                    lattice_flag = True
        return lattice_vectors

    def parse_atomic_postions(a_p, elements):
        for index in range(len(a_p)):
            if (index % 4) == 0:
                # initial addition of element
                if len(elements) == 0:
                    # adds the element and its properties to the list
                    elements.append(atom(a_p[index], a_p[index + 1], a_p[index + 2], a_p[index + 3]))
                    # manually increase the length of the vectors
                    elements[-1].increase_length()
                else:
                    for j in range(len(elements)):
                        if a_p[index] == elements[j].get_symbol():
                            elements[j].add_vector(a_p[index + 1], a_p[index + 2], a_p[index + 3])
                            break
                        elif j == (len(elements) - 1):
                            # adds the element and its properties to the list
                            elements.append(atom(a_p[index], a_p[index + 1], a_p[index + 2], a_p[index + 3]))
                            # manually increase the length of the vectors
                            elements[-1].increase_length()
        return elements

    # iterates through the list of lines looking for the atomic positions:
    # uses a regex to look for the lattice vectors depending on the file type format
    # site n.     atom                  positions (alat units)  <-*.scf.*
    def get_atomic_positions(lines=[], file_type='', file_format=''):
        elements = []

        if file_format == 'vc-relax':
            # bound for the atomic position parsing
            atomic_positions_bound = 0
            # iterate through all the lines in the list
            for line in lines:
                atomic_positions_bound += 1
                # break out of the loop when key word is found
                if 'ATOMIC_POSITIONS' in line:
                    break
            ato_pos = lines[atomic_positions_bound:]
            atomic_positions = []
            # format the list to remove redundant spacing
            for at_po in ato_pos:
                atomic_positions.append(re.sub(r'\s+', ' ', at_po))

            if file_type == 'unfinished':
                atomic_positions = list(filter(None, atomic_positions))

            a_p = []
            # add elements to the list of objects
            for ap in atomic_positions:
                for index in range(len(ap.split(' '))):
                    if ap.split(' ')[index] != '0':
                        if len(elements) is 0:
                            a_p.append(ap.split(' ')[index])

            # adds the atomic positions to the list of element classes
            elements = parse_atomic_postions(a_p, elements)

        # input file was in scf format
        elif file_format == 'scf' and file_type == 'out':
            # bound for the atomic position parsing
            atomic_positions_bound = 0
            # iterate through all the lines in the list
            for line in lines:
                atomic_positions_bound += 1
                # break out of the loop when key word is found
                if 'site n' in line:
                    break
            ato_pos = lines[atomic_positions_bound:]
            atomic_positions = []
            # regex to remove all non number, non letter and non period characters
            regex = re.compile(r'[^A-Za-z0-9.]+')
            # format the list to remove redundant spacing
            for at_po in ato_pos:
                atomic_positions.append(regex.sub('_', at_po.strip())[:-1])
            a_p = []
            # add elements to the list of objects
            for ap in atomic_positions:
                for index in range(len(ap.split('_'))):
                    if ap.split('_')[index].isdigit() and len(ap.split('_')[index]) > 1:
                        a_p.append(ap.split('_')[index])
                    if not ap.split('_')[index].isdigit() and ap.split('_')[index] != 'tau':
                        a_p.append(ap.split('_')[index])
            # adds the atomic positions to the list of element classes
            a_p = a_p[:-1]
            elements = parse_atomic_postions(a_p,elements)
        return elements

    input_file_path = ''
    file_format = ''

    if argv[1] == '-help' or argv[1] == 'help' or argv[1] == 'h':
        display_help()
        exit()

    # read from standard input mode
    if argv[1] == '-stdin':
        input_file_path = '{}.{}.{}.out'.format(argv[2], argv[3], argv[4])
        with open(input_file_path, 'w') as data_file:
            if not stdin.isatty():
                lines = stdin
                for line in lines:
                    data_file.write(line)

    else:
        # file to be parsed (including path)
        input_file_path = argv[1]

    # call to check the inputted file
    check_file(input_file_path)

    # assigns both the file type and format
    file_type = input_file_path.split('.')[-1]

    for w in input_file_path.split('.'):
        if w == 'vc-relax' or w == 'scf':
            file_format = w

    # if the user does not wish to change the directory
    output_file_path = ''

    # the user wants to save the file in a new directory
    if len(argv) == 3 or len(argv) == 6:
        # sets the output file path to a new location
        output_file_path = argv[len(argv) - 1]

    # parses the file based on the type and format of the file
    lines = parse_file(file_type, file_format, input_file_path)
    file_name = ''
    if argv[1] == '-stdin':
        file_name = '{}.{}.'.format(argv[2], argv[3])
    else:
        file_name = ''.join(str(e + '.') for e in input_file_path.split('/')[-1].split('.')[0:2])
    print(output_file_path)
    # opens/creates output file to write
    with open('{}{}POSCAR.VASP'.format(output_file_path, file_name), 'w') as out_file:

        # writes the first line [Symbols] [Symmetry group]
        out_file.write(''.join(str(e + ' ') for e in input_file_path.split('/')[-1].split('.')[0:2]))

        out_file.write('\n')
        # three spaces for the current line
        out_file.write('   ')
        # element 9 will be the line with the lattice parameter
        # regex to remove all non-numerical characters except the "."
        out_file.write(get_lattice_parameter(lines, file_format))
        out_file.write('\n')

        lattice_vectors = get_lattice_vectors(lines, file_type, file_format)

        index = 0
        # write the lattice vectors to file
        for index in range(len(lattice_vectors)):
            # case 1: first component is negative
            if lattice_vectors[index][0] == '-' and (index is 0 or index is 3 or index is 6):
                out_file.write('    {}'.format(lattice_vectors[index]))

            # case 2: first component is not negative
            elif lattice_vectors[index][0] != '-' and (index is 0 or index is 3 or index is 6):
                out_file.write('     {}'.format(lattice_vectors[index]))

            # case 3: non-first component is negative
            elif lattice_vectors[index][0] == '-' and (index is not 0 or index is not 3 or index is not 6):
                out_file.write('   {}'.format(lattice_vectors[index]))

            # case 3: non-first component is not negative
            elif lattice_vectors[index][0] != '-' and (index is not 0 or index is not 3 or index is not 6):
                out_file.write('    {}'.format(lattice_vectors[index]))

            # new line after the last component in the vector
            if index is 2 or index is 5 or index is 8:
                out_file.write('\n')

        elements = get_atomic_positions(lines, file_type, file_format)

        out_file.write('   ')
        # rows for elements and length
        for row in range(2):
            # columns
            for e in elements:
                # first row (symbols)
                if row == 0:
                    out_file.write(e.get_symbol())
                    out_file.write('   ')
                # second row (amount of vectors)
                else:
                    out_file.write(str(e.leng()))
                    out_file.write('  ')

            out_file.write('\n')
            if row != 1:
                out_file.write('     ')

        out_file.write('Direct')
        out_file.write('\n')

        for e in elements:
            # rows
            for row in range(e.leng()):
                # case 1: first component is negative
                if e.get_x_pos(row)[0] == '-':
                    out_file.write('     {}'.format(e.get_x_pos(row)))

                # case 2: first component is not negative
                if e.get_x_pos(row)[0] != '-':
                    out_file.write('      {}'.format(e.get_x_pos(row)))

                # case 3: second component is negative
                if e.get_y_pos(row)[0] == '-':
                    out_file.write('  {}'.format(e.get_y_pos(row)))

                # case 4: second component is not negative
                if e.get_y_pos(row)[0] != '-':
                    out_file.write('   {}'.format(e.get_y_pos(row)))

                # case 5: third component is negative
                if e.get_z_pos(row)[0] == '-':
                    out_file.write('  {}'.format(e.get_z_pos(row)))
                    out_file.write('\n')

                # case 6: third component is not negative
                if e.get_z_pos(row)[0] != '-':
                    out_file.write('   {}'.format(e.get_z_pos(row)))
                    out_file.write('\n')
        out_file.write('\n')
        total_elements = 0

        # get total amount of elements
        for e in elements:
            total_elements += e.leng()

        for i in range(total_elements):
            out_file.write('  0.00000000E+00  0.00000000E+00  0.00000000E+00')
            out_file.write('\n')


if __name__ == '__main__':
    main()
