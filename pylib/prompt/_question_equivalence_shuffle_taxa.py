import typing

from ..treeprep._shuffle_taxa_newick import shuffle_taxa_newick
from ._shuffle_choices import shuffle_choices


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

    choices, answer = shuffle_choices(choices, answer)

    swapped_newick_string = shuffle_taxa_newick(newick_string)
    return question, choices, answer, [newick_string, swapped_newick_string]
