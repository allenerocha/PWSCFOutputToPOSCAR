"""This module parses the given file and returns the useful data as a list"""
import sys


def parse_file(file_type: str, file_format: str, input_file_path: str) -> list:
    """Goes through the file to extract the useful information
    return: None
    Args:
        file_type (str): file extension :param file_format: format of the file
        file_format (str): file extension
        input_file_path (str): location of the file
    """
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

            if file_type == 'out':
                # iterates through the file adding each of the lines to the list
                for line in in_file:
                    # adds the current line of the string to the list
                    lines.append(line.strip())
                    # checks if the upper bound flag has been tripped
                    if upper_bound_flag is False:
                        # increments until the upper bound flag is tripped
                        upper_bound += 1
                    # checks if the current line is the flag
                    if file_type == 'out' and file_format == 'vc-relax':
                        if line.strip() == 'Final estimate of lattice vectors (input alat units)':
                            upper_bound_flag = True
                        # checks for lower bound
                        if line.strip() == 'End final coordinates':
                            # lower bound found, breaks out of the code to save some time
                            break
                    # increment the lower bound integer
                    elif file_type == 'out' and file_format == 'scf':
                        # checks if the current line is the flag
                        if 'bravais-lattice index' in line.strip():
                            # trips the upper bound flag
                            upper_bound_flag = True
                        # checks for lower bound
                        if 'number of k points' in line.strip():
                            # lower bound found, breaks out of the code to save some time
                            break
                    else:
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
    except FileNotFoundError as file_not_found_exception:
        print(str(file_not_found_exception))
        sys.exit()
