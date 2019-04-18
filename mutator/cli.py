from .mutator import mutate


def main():
    sequences = {
        'reference': 'aaaccczfff',
        'other_one': 'aaeee',
        'other_three': 'ggg'
    }

    operations = [
        {
            'type': 'deletion_insertion',
            'source': 'reference',
            'location': {
                'type': 'range',
                'start': {
                    'type': 'point',
                    'position': 3
                },
                'end': {
                    'type': 'point',
                    'position': 4
                }
            },
            'inserted': [
                {
                    'sequence': 'bbb',
                    'source': 'description'
                }
            ]
        }
    ]

    print(mutate(sequences, operations))
