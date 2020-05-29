# Assumptions for which we do not check:
# - only 'deletion_insertion' operations.
# - only exact locations.
# - start > end.
# - no overlapping.
# Note that if any of the above is not met, the result will be bogus.
#
# Other assumptions:
# - there can be empty inserted lists.


from .util import reverse_complement


def get_inverted(sequence):
    """
    Reverse complement inversion using code extracted from BioPython.
    """
    return reverse_complement(sequence)


def get_start_end(location):
    """
    Get the start and the end of a location object. For point locations both
    start and end equal the position value.
    """
    if location['type'] == 'range':
        return location['start']['position'], location['end']['position']
    elif location['type'] == 'point':
        return location['position'], location['position']


def get_inserted_sequence(inserted, sequences):
    """
    Retrieves the actual sequence mentioned in the insertion.
    """
    if inserted['source'] == 'description':
        sequence = inserted['sequence']
    else:
        sequence = sequences[inserted['source']][slice(
            *get_start_end(inserted['location']))]
    if inserted.get('inverted'):
        sequence = get_inverted(sequence)
    return sequence


def mutate(sequences, variants):
    """
    Mutates the reference sequence according to the provided operations.

    :param sequences: sequences dictionary.
    :param variants: operations list.
    :return: the mutated `sequences['reference']` sequence.
    """
    reference = sequences['reference']

    variants = sorted(variants, key=lambda v: (get_start_end(v['location'])))

    parts = []
    current_index = 0
    for variant in variants:
        start, end = get_start_end(variant['location'])
        parts.append(reference[current_index:start])
        for insertion in variant['inserted']:
            parts.append(get_inserted_sequence(insertion, sequences))
        current_index = end

    parts.append(reference[current_index:])

    return ''.join(parts)
