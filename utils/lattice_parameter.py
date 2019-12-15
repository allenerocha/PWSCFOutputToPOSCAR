"""This module is used to retrieve the lattice parameter from the data"""
import re


def get_lattice_parameter(lines: list, file_format: str) -> str:
    """
    Uses a regular expression to filter find the lattice parameter
    :param lines: list of the saved lines from the input file
    :param file_format: formatting of the file
    :return: None
    """
    # input file was in vc-relax format
    if lines is None:
        lines = []
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
