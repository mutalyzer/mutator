import pytest
from mutator import mutate


def get_location(start, end=None):
    if end:
        return {"type": "range", "start": get_location(start), "end": get_location(end)}
    else:
        return {"type": "point", "position": start}


def test_basic():
    sequences = {"reference": "aaaacczfff", "other_one": "bc", "other_three": "ggg"}

    variants = [
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": get_location(3, 4),
            "inserted": [{"source": "description", "sequence": "bb"}],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": get_location(4, 4),
            "inserted": [{"source": "other_one", "location": get_location(0, 10)}],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": get_location(6, 7),
            "inserted": [],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": get_location(7, 7),
            "inserted": [{"source": "description", "sequence": "ddd"}],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": get_location(8, 9),
            "inserted": [{"source": "description", "sequence": "ggg"}],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": get_location(9, 10),
            "inserted": [{"source": "description", "sequence": "hhh"}],
        },
    ]

    assert mutate(sequences, variants) == "aaabbbcccdddfggghhh"


REFERENCE = "ACGTCGATTCGCTAGCTTCGGGGGATAGATAGAGATATAGAGAT"

# The following descriptions use HGVS locations, while variants use internal.
TESTS = [
    ("(empty)", {"reference": "", "observed": ""}, []),
    ("=", {"reference": REFERENCE, "observed": REFERENCE}, []),
    (
        "0_1insT",  # In HGVS this does't seem possible.
        {"reference": "AAA", "observed": "TAAAA"},
        [
            {
                "type": "deletion_insertion",
                "location": get_location(0, 0),
                "inserted": [{"source": "description", "sequence": "TA"}],
            }
        ],
    ),
    (
        "3_4insT",  # Where an insertion can firstly take place in HGVS?
        {"reference": "AAA", "observed": "AAATA"},
        [
            {
                "type": "deletion_insertion",
                "location": get_location(3, 3),
                "inserted": [{"source": "description", "sequence": "TA"}],
            }
        ],
    ),
    (
        "1A>T",
        {
            "reference": REFERENCE,
            "observed": "TCGTCGATTCGCTAGCTTCGGGGGATAGATAGAGATATAGAGAT",
        },
        [
            {
                "type": "deletion_insertion",
                "location": get_location(0, 1),
                "inserted": [{"source": "description", "sequence": "T"}],
            }
        ],
    ),
    (
        "44_45insT",
        {
            "reference": REFERENCE,
            "observed": "TACGTCGATTCGCTAGCTTCGGGGGATAGATAGAGATATAGAGAT",
        },
        [
            {
                "type": "deletion_insertion",
                "location": get_location(0, 0),
                "inserted": [{"source": "description", "sequence": "T"}],
            }
        ],
    ),
    (
        "7A>G",
        {
            "reference": REFERENCE,
            "observed": "ACGTCGGTTCGCTAGCTTCGGGGGATAGATAGAGATATAGAGAT",
        },
        [
            {
                "type": "deletion_insertion",
                "location": get_location(6, 7),
                "inserted": [{"source": "observed", "location": get_location(6, 7)}],
            }
        ],
    ),
    (
        "7del",
        {
            "reference": REFERENCE,
            "observed": "ACGTCGTTCGCTAGCTTCGGGGGATAGATAGAGATATAGAGAT",
        },
        [
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(6, 7),
                "inserted": [{"source": "observed", "location": get_location(6, 6)}],
            }
        ],
    ),
    (
        "7_8del",
        {
            "reference": REFERENCE,
            "observed": "ACGTCGTCGCTAGCTTCGGGGGATAGATAGAGATATAGAGAT",
        },
        [
            {
                "type": "deletion_insertion",
                "inserted": [{"source": "observed", "location": get_location(6, 6)}],
                "source": "reference",
                "location": get_location(6, 8),
            }
        ],
    ),
    (
        "6_7insC",
        {
            "reference": REFERENCE,
            "observed": "ACGTCGCATTCGCTAGCTTCGGGGGATAGATAGAGATATAGAGAT",
        },
        [
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(6, 6),
                "inserted": [{"source": "observed", "location": get_location(6, 7)}],
            }
        ],
    ),
    (
        "[26A>C;30C>A;35G>C]",
        {
            "reference": "TAAGCACCAGGAGTCCATGAAGAAGATGGCTCCTGCCATGGAATCCCCTACTCTACTGTG",
            "observed": "TAAGCACCAGGAGTCCATGAAGAAGCTGGATCCTCCCATGGAATCCCCTACTCTACTGTG",
        },
        [
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(25, 26),
                "inserted": [{"source": "observed", "location": get_location(25, 26)}],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(29, 30),
                "inserted": [{"source": "observed", "location": get_location(29, 30)}],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(34, 35),
                "inserted": [{"source": "observed", "location": get_location(34, 35)}],
            },
        ],
    ),
    (
        "[30C>A;35G>C;26A>C]",
        {
            "reference": "TAAGCACCAGGAGTCCATGAAGAAGATGGCTCCTGCCATGGAATCCCCTACTCTACTGTG",
            "observed": "TAAGCACCAGGAGTCCATGAAGAAGCTGGATCCTCCCATGGAATCCCCTACTCTACTGTG",
        },
        [
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(29, 30),
                "inserted": [{"source": "observed", "location": get_location(29, 30)}],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(34, 35),
                "inserted": [{"source": "observed", "location": get_location(34, 35)}],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(25, 26),
                "inserted": [{"source": "observed", "location": get_location(25, 26)}],
            },
        ],
    ),
    (
        "37_38ins3_26inv",
        {
            "reference": "ATGGCGGCGGTGGTCGCCCTCTCCTTGAGGCGCCGGTTGCCGGCCACAACCCTTGGCGGA",
            "observed": "ATGGCGGCGGTGGTCGCCCTCTCCTTGAGGCGCCGGTAAGGAGAGGGCGACCACCGCCGCCTGCCGGCCACAACCCTTGGCGGA",
        },
        [
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(37, 37),
                "inserted": [
                    {
                        "source": "reference",
                        "location": get_location(2, 26),
                        "inverted": True,
                    }
                ],
            }
        ],
    ),
    (
        "[3_4insT;4_5insCC;2_3insG]",
        {"reference": "AAAATTTT", "observed": "AAGATACCTTTT"},
        [
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(3, 3),
                "inserted": [{"source": "description", "sequence": "T"}],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(4, 4),
                "inserted": [{"source": "description", "sequence": "CC"}],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": get_location(2, 2),
                "inserted": [{"source": "description", "sequence": "G"}],
            },
        ],
    ),
]


@pytest.mark.parametrize("_, sequences, variants", TESTS)
def test_variants_de_extracts(_, sequences, variants):
    assert sequences["observed"] == mutate(sequences, variants)
