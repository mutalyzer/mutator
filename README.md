This library provides an interface to mutate a DNA reference sequence
according to a list of variants.

# Installation

The software is distributed via PyPI. It can be installed with `pip`:

```sh
pip install mutalyzer-mutator
```

## From source

To install the latest development version, use the following commands:

```sh
git clone https://github.com/mutalyzer/mutator.git
cd mutator
pip install .
```

# Usage

```python
from mutalyzer_mutator import mutate

sequences = {"reference": "AAGG", "other": "AATTAA"}

variants = [
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
                "source": "other",
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
```
