import typing

from ..treeprep._swap_taxa_newick import swap_taxa_newick


def question_equivalence_swap_taxa(
    newick_string: str,
    taxa: typing.Optional[typing.Sequence[str]] = None,
) -> tuple[str, list[str], int, list[str]]:

    question = (
        f"Do the two given phylogenies represent the same tree structure?"
    )
    choices = [
        f"yes, the phylogenies are equivalent",
        f"no, the phylogenies are different",
    ]

    answer = 1

    swapped_newick_string = swap_taxa_newick(newick_string)
    return question, choices, answer, [newick_string, swapped_newick_string]
