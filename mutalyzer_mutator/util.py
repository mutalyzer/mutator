# The following code is adapted from biopython 1.77:
# - https://github.com/biopython/biopython/blob/biopython-177/Bio/Seq.py
# - https://github.com/biopython/biopython/blob/biopython-177/Bio/Data/IUPACData.py
# Notes:
# - The alphabet check was removed - no errors are raised.


ambiguous_dna_complement = {
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A",
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
     - complement_mapping - a dictionary such as ambiguous_dna_complement
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
    Return the complement sequence by creating a new Seq object.
    >>> sequence = 'CCCCCGATAG'
    >>> complement(sequence)
    'GGGGGCTATC'

    You can of course used mixed case sequences,

    >>> sequence = 'CCCCCgatA-GD'
    >>> complement(sequence)
    'GGGGGctaT-CH'

    Note in the above example, ambiguous character D denotes
    G, A or T so its complement is H (for C, T or A).
    """
    translation_table = _maketrans(ambiguous_dna_complement)
    return sequence.translate(translation_table)


def reverse_complement(sequence):
    """
    Return the reverse complement sequence.

    >>> sequence = 'CCCCCGATAGNR'
    >>> reverse_complement(sequence)
    'YNCTATCGGGGG'

    Note in the above example, since R = G or A, its complement
    is Y (which denotes C or T).

    You can of course used mixed case sequences,

    >>> sequence = 'CCCCCgatA-G'
    >>> reverse_complement(sequence)
    'C-TatcGGGGG'
    """
    # Use -1 stride/step to reverse the complement
    return complement(sequence)[::-1]
