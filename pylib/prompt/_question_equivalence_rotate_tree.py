import typing

from ..treeprep._rotate_phylogeny_newick import rotate_phylogeny_newick


def question_equivalence_rotate_tree(
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

    answer = 0

    rotated_newick_string = rotate_phylogeny_newick(newick_string)
    return question, choices, answer, [newick_string, rotated_newick_string]