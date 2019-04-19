# locations are
#
# Assumptions for which we do not check:
# - only exact locations.
# - start > end.
# - no overlapping.
# - sorted locations.
# Other assumptions:
# - there can be empty inserted lists.
# Note that if any of the above is not met, the result will be bogus.


def get_start_end(location):
    """
    Get the start and the end of a location object. For point locations both
    start and end equal the position value.
    """
    if location['type'] == 'range':
        return location['start']['position'],\
               location['end']['position']
    elif location['type'] == 'point':
        return location['position'],\
               location['position']


def get_inserted_sequence(insertion, sequences):
    """
    Retrieves the actual sequence mentioned in the insertion.
    """
    if insertion['source'] is 'description':
        return insertion['sequence']
    else:
        return sequences[insertion['source']][slice(
            *get_start_end(insertion['location']))]


def mutate(sequences, operations):
    """
    Mutates the reference sequence according to the provided operations.

    :param sequences: sequences dictionary.
    :param operations: operations list.
    :return: the mutated `sequences['reference']` sequence.
    """
    reference = sequences['reference']

    parts = []
    iterator = 0
    for operation in operations:
        start, end = get_start_end(operation['location'])
        parts.append(reference[iterator:start])
        for insertion in operation['inserted']:
            print(get_inserted_sequence(insertion, sequences))
            parts.append(get_inserted_sequence(insertion, sequences))
        iterator = end

    observed = ''.join(parts)

    return observed
