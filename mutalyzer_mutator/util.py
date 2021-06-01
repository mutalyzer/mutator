"""
Various util functions.

The following code is adapted from biopython 1.77:
  - https://github.com/biopython/biopython/blob/biopython-177/Bio/Seq.py
  - https://github.com/biopython/biopython/blob/biopython-177/Bio/Data/IUPACData.py

Notes:
  - The alphabet check was removed.
  - No previous custom errors are raised any longer.
"""

ambiguous_complement = {
    "A": "T",
    "a": "u",
    "C": "G",
    "G": "C",
    "T": "A",
    "u": "a",
    "M": "K",
    "R": "Y",
    "W": "W",
    "S": "S",
    "Y": "R",
    "K": "M",
    "V": "B",
    "H": "D",
    "D": "H",
    "B": "V",
    "X": "X",
    "N": "N",
}


def _maketrans(complement_mapping):
    """
    Make a python string translation table (PRIVATE).

    Arguments:
     - complement_mapping - a dictionary such as ambiguous_complement
       and ambiguous_rna_complement from Data.IUPACData.

    Returns a translation table (a string of length 256) for use with the
    python string's translate method to use in a (reverse) complement.

    Compatible with lower case and upper case sequences.

    For internal use only.
    """
    before = "".join(complement_mapping.keys())
    after = "".join(complement_mapping.values())
    before += before.lower()
    after += after.lower()
    return str.maketrans(before, after)


def complement(sequence):
    """
    Complement the ``sequence``.

    >>> sequence = 'CCCCCGATAG'
    >>> complement(sequence)
    'GGGGGCTATC'

    You can use mix DNA with RNA sequences.

    >>> sequence = 'CCCCCaTuAGD'
    >>> complement(sequence)
    'GGGGGuAaTCH'

    Also, you can use mixed case sequences.

    >>> sequence = 'CCCCCgatA-GD'
    >>> complement(sequence)
    'GGGGGcuaT-CH'

    Note that in the above example, the ambiguous character ``D`` denotes
    ``G``, ``A`` or ``T`` so its complement is ``H`` (for ``C``, ``T`` or
    ``A``).

    :arg str sequence: Input sequence.
    :returns: Complemented sequence.
    :rtype: str
    """
    translation_table = _maketrans(ambiguous_complement)
    return sequence.translate(translation_table)


def reverse_complement(sequence):
    """
    Reverse complement the ``sequence``.

    >>> sequence = 'CCCCCGATAGNR'
    >>> reverse_complement(sequence)
    'YNCTATCGGGGG'

    Note that in the above example, since ``R`` = ``G`` or ``A``,
    its complement is ``Y`` (which denotes ``C`` or ``T``).

    You can use mix DNA with RNA sequences.

    >>> sequence = 'CCCCCaTuAGD'
    >>> reverse_complement(sequence)
    'HCTaAuGGGGG'

    You can of course used mixed case sequences,

    >>> sequence = 'CCCCCgatA-G'
    >>> reverse_complement(sequence)
    'C-TaucGGGGG'

    :arg str sequence: Input sequence.
    :returns: Reverse complemented sequence.
    :rtype: str
    """
    return complement(sequence)[::-1]
