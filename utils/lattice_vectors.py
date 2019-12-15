"""This module retrieves the lattice vectors"""


def get_lattice_vectors(lines: list, file_format: str) -> list:
    """
    Parses the lattice vectors from the lines passed
    :param lines: list of lines parsed from the data entry
    :param file_format: format of the data
    :return: lattice vectors as a list
    """
    lattice_vectors = []
    # input file was in vc-relax format
    # add the sublist of lattice vectors from the
    # first three elements of the lines list
    index = 0
    lattice_flag = False
    for line in lines:
        if file_format == 'vc--relax':
            if 'unit-cell' in line:
                break
            for word in line.split(' '):
                if word != '':
                    lattice_vectors.append(word)
        else:
            if lattice_flag:
                for word in line.split(' '):
                    if not word.isalpha() and '.' in word:
                        lattice_vectors.append(word)
                index += 1
                if index > 2:
                    break
                if 'crystal axes:' in line:
                    lattice_flag = True
    return lattice_vectors
