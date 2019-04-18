# To be decided  (for the moment):
# - Do we consider only exact locations? (yes)
# - Do we discard locations for which start > end? (yes)
# - Do we fail hard in case of deletions overlap? (yes)
# - Do we assume the order important? (yes)


def point_checks(point):
    if not isinstance(point, dict):
        raise ValueError
    if point.get('type') is None:
        raise ValueError
    if point['type'] is not 'point':
        raise ValueError
    if point.get('position') is None:
        raise ValueError


def location_checks(location):
    if not isinstance(location, dict):
        raise ValueError
    if location.get('type') is None:
        raise ValueError
    if location['type'] not in ['range', 'point']:
        raise ValueError
    if location['type'] is 'range':
        if location.get('start') is None:
            raise ValueError
        point_checks(location['start'])
        if location.get('end') is None:
            raise ValueError
        point_checks(location['end'])
        if location['start']['position'] > \
                location['end']['position']:
            raise ValueError


def operation_checks(operation):
    """
    Checking if an operation can be utilized in terms of schema.

    Note: Maybe it should be replaced with the schema validation from the
    normalizer, or a customized schema should be derived.
    """
    if operation.get('type') is not 'deletion_insertion':
        raise ValueError
    if operation.get('location') is None:
        raise ValueError
    location_checks(operation['location'])


def operations_check(operations):
    """
    Some sanity checking.
    """
    for operation in operations:
        operation_checks(operation)


def is_overlap(operations):
    return False


def get_start_end(operation):
    if operation['location']['type'] is 'range':
        return operation['location']['start']['point'],\
               operation['location']['end']['point']
    elif operation['location']['type'] is 'point':
        return operation['location']['point'], operation['location']['point']


def mutate(sequences, operations):

    operations_check(operations)
    if is_overlap(operations):
        raise ValueError

    observed = sequences['reference']

    for operation in operations:
        start, end = get_start_end(operation)


    return observed
