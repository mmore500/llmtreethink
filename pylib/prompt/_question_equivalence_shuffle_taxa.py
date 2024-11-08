import typing

from ..treeprep._shuffle_taxa_newick import shuffle_taxa_newick


def question_equivalence_shuffle_taxa(
    newick_string: str,
    taxa: typing.Optional[typing.Sequence[str]] = None,
) -> tuple[str, list[str], int, list[str]]:

    question = (
        "Do the two given phylogenies represent the same evolutionary history?"
    )
    choices = [
        "yes, the phylogenies are equivalent",
        "no, the phylogenies are different",
    ]

    answer = 1

    swapped_newick_string = shuffle_taxa_newick(newick_string)
    return question, choices, answer, [newick_string, swapped_newick_string]
