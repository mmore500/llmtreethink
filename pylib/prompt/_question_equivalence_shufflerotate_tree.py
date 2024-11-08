import random
import typing

import dendropy as dp

from ..treeprep._rotate_phylogeny_newick import rotate_phylogeny_newick
from ._shuffle_choices import shuffle_choices


def question_equivalence_shufflerotate_tree(
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

    answer = 0

    choices, answer = shuffle_choices(choices, answer)

    tree = dp.Tree.get(data=newick_string, schema="newick")
    for node in tree.preorder_node_iter():
        child_nodes = node.child_nodes()
        random.shuffle(child_nodes)
        node.clear_child_nodes()
        node.set_child_nodes(child_nodes)

    rotated_newick_string = rotate_phylogeny_newick(tree.as_string("newick"))
    return question, choices, answer, [newick_string, rotated_newick_string]
