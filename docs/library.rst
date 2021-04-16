Usage
=====

The ``mutate()`` function provides an interface to mutate a sequence according
to a list of variants. A dictionary with the reference ids as keys and their
sequences as values should be provided as input. The reference with the
``reference`` key is the one to be mutate according to the variants model
list, the second input of the ``mutate()`` function.

.. code-block:: python

    from mutalyzer_mutator import mutate

    sequences = {"reference": "AAGG", "OTHER_REF": "AATTAA"}

    variants = [
        # 2_2delinsOTHER_REF:2_4
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": {
                "type": "range",
                "start": {"type": "point", "position": 2},
                "end": {"type": "point", "position": 2},
            },
            "inserted": [
                {"sequence": "CC", "source": "description"},
                {
                    "source": {"id": "OTHER_REF"},
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 2},
                        "end": {"type": "point", "position": 4},
                    },
                },
            ],
        }
    ]

    observed = mutate(sequences, variants)  # observed = 'AACCTTGG'
