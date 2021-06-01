import pytest

from mutalyzer_mutator.mutator import UnknownInsertedSource, mutate


def _location(start, end=None):
    if end:
        return {"type": "range", "start": _location(start), "end": _location(end)}
    else:
        return {"type": "point", "position": start}


def test_basic():
    sequences = {"reference": "aaaacczfff", "other_one": "bc", "other_three": "ggg"}

    variants = [
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": _location(3, 4),
            "inserted": [{"source": "description", "sequence": "bb"}],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": _location(4, 4),
            "inserted": [{"source": {"id": "other_one"}, "location": _location(0, 10)}],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": _location(6, 7),
            "inserted": [],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": _location(7, 7),
            "inserted": [{"source": "description", "sequence": "ddd"}],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": _location(8, 9),
            "inserted": [{"source": "description", "sequence": "ggg"}],
        },
        {
            "type": "deletion_insertion",
            "source": "reference",
            "location": _location(9, 10),
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
                "location": _location(0, 0),
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
                "location": _location(3, 3),
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
                "location": _location(0, 1),
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
                "location": _location(0, 0),
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
                "location": _location(6, 7),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(6, 7)}
                ],
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
                "location": _location(6, 7),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(6, 6)}
                ],
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
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(6, 6)}
                ],
                "source": "reference",
                "location": _location(6, 8),
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
                "location": _location(6, 6),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(6, 7)}
                ],
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
                "location": _location(25, 26),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(25, 26)}
                ],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": _location(29, 30),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(29, 30)}
                ],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": _location(34, 35),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(34, 35)}
                ],
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
                "location": _location(29, 30),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(29, 30)}
                ],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": _location(34, 35),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(34, 35)}
                ],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": _location(25, 26),
                "inserted": [
                    {"source": {"id": "observed"}, "location": _location(25, 26)}
                ],
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
                "location": _location(37, 37),
                "inserted": [
                    {
                        "source": "reference",
                        "location": _location(2, 26),
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
                "location": _location(3, 3),
                "inserted": [{"source": "description", "sequence": "T"}],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": _location(4, 4),
                "inserted": [{"source": "description", "sequence": "CC"}],
            },
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": _location(2, 2),
                "inserted": [{"source": "description", "sequence": "G"}],
            },
        ],
    ),
    (
        "[1_2del;5_5insAT]",
        {"reference": "AAAATTTT", "observed": "AAATATTTT"},
        [
            {
                "type": "deletion_insertion",
                "location": _location(1, 2),
                "inserted": [],
            },
            {
                "type": "deletion_insertion",
                "location": _location(5, 5),
                "inserted": [{"source": "description", "sequence": "AT"}],
            },
        ],
    ),
    (
        "[0_4delinsA[6]]",
        {"reference": "AAAATTTT", "observed": "AAAAAATTTT"},
        [
            {
                "type": "deletion_insertion",
                "location": _location(0, 4),
                "inserted": [
                    {
                        "source": "description",
                        "sequence": "A",
                        "repeat_number": {"value": 6},
                    }
                ],
            }
        ],
    ),
    (
        "[0_4delins[A[6];del6_7]",
        {"reference": "AAAATTTT", "observed": "AAAAAATTT"},
        [
            {
                "type": "deletion_insertion",
                "location": _location(0, 4),
                "inserted": [
                    {
                        "source": "description",
                        "sequence": "A",
                        "repeat_number": {"value": 6},
                    }
                ],
            },
            {
                "type": "deletion_insertion",
                "location": _location(6, 7),
                "inserted": [],
            },
        ],
    ),
    (
        "[3_6delins3_6[6]inv]",
        {"reference": "AAAATTTT", "observed": "AAAAATAATAATAATAATAATTT"},
        [
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": _location(3, 6),
                "inserted": [
                    {
                        "source": "reference",
                        "location": _location(3, 6),
                        "repeat_number": {"value": 6},
                        "inverted": True,
                    }
                ],
            }
        ],
    ),
    (
        "[3_6delins3_6[6]inv]",
        {"reference": "AAaauuTT", "observed": "AAaaauaauaauaauaauaauTT"},
        [
            {
                "type": "deletion_insertion",
                "source": "reference",
                "location": _location(3, 6),
                "inserted": [
                    {
                        "source": "reference",
                        "location": _location(3, 6),
                        "repeat_number": {"value": 6},
                        "inverted": True,
                    }
                ],
            }
        ],
    ),
]


@pytest.mark.parametrize("_, sequences, variants", TESTS)
def test_variants_de_extracts(_, sequences, variants):
    assert sequences["observed"] == mutate(sequences, variants)


@pytest.mark.parametrize(
    "sequences, variants",
    [
        (
            {"reference": "AAA"},
            [
                {
                    "type": "deletion_insertion",
                    "location": _location(3, 3),
                    "inserted": [{"source": "not_supported", "sequence": "TA"}],
                }
            ],
        ),
    ],
)
def test_unknown_inserted_source(sequences, variants):
    with pytest.raises(UnknownInsertedSource):
        mutate(sequences, variants)
