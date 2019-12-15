"""This module is used to retreive the atomic positions of the atoms"""
import re

from atom.atom import Atom


def get_atomic_positions(lines: list, file_type: str, file_format: str) -> list:
    """
    Retrieves the atomic positions from the cleaned lines
    :param lines: lines of the data
    :param file_type: file extension
    :param file_format: formatting of the data
    :return: list of the atomic positions
    """

    if file_format == 'vc-relax':
        return _vc_format(lines, file_type)

    # input file was in scf format
    return _scf_format(lines)


def _vc_format(lines: list, file_type: str):
    elements = list()
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
    for atom_position in atomic_positions:
        for index in range(len(atom_position.split(' '))):
            if atom_position.split(' ')[index] != '0':
                if len(elements) == 0:
                    a_p.append(atom_position.split(' ')[index])

    # adds the atomic positions to the list of element classes
    return _parse_atomic_positions(a_p, elements)


def _scf_format(lines: list):
    elements = list()
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
    for atom_position in atomic_positions:
        for index in range(len(atom_position.split('_'))):
            if atom_position.split('_')[index].isdigit() \
                    and len(atom_position.split('_')[index]) > 1:
                a_p.append(atom_position.split('_')[index])
            if not atom_position.split('_')[index].isdigit() \
                    and atom_position.split('_')[index] != 'tau':
                a_p.append(atom_position.split('_')[index])
    # adds the atomic positions to the list of element classes
    a_p = a_p[:-1]
    return _parse_atomic_positions(a_p, elements)


def _parse_atomic_positions(atomic_positions: list, elements: list) -> list:
    """
    Cleans the atomic positions from the list of lines
    :param atomic_positions: Uncleaned lines containing the atomic positions
    :param elements: list of elements
    :return: Cleaned list of the atomic positions
    """
    for i, atom in enumerate(atomic_positions):
        if (i % 4) == 0:
            # initial addition of element
            if len(elements) == 0:
                # adds the element and its properties to the list
                elements.append(Atom(atom, atomic_positions[i + 1],
                                     atomic_positions[i + 2],
                                     atomic_positions[i + 3]))
                # manually increase the length of the vectors
                elements[-1].increment_size()
            else:
                for j, _ in enumerate(elements):
                    if atomic_positions[i] == elements[j].get_symbol():
                        elements[j].add_vector(atomic_positions[i + 1],
                                               atomic_positions[i + 2],
                                               atomic_positions[i + 3])
                    elif j == (len(elements) - 1):
                        # adds the element and its properties to the list
                        elements.append(Atom(atom, atomic_positions[i + 1],
                                             atomic_positions[i + 2],
                                             atomic_positions[i + 3]))
                        # manually increase the length of the vectors
                        elements[-1].increment_size()
    return elements
