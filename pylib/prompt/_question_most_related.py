import random
import typing

import dendropy as dp
import numpy as np


def question_identify_most_related(
    newick_string: str,
    taxa: typing.Optional[typing.Sequence[str]] = None,
) -> tuple[str, list[str], int]:

    tree = dp.Tree.get(data=newick_string, schema="newick")
    for node in tree.preorder_node_iter():
        node.edge.length = 1.0

    if taxa is None:
        taxa = random.sample(
            [x.taxon.label for x in tree.leaf_nodes()],
            3,
        )

    first, second, third = taxa
    question = f"Which pair among {first}, {second}, and {third} are most closely related?"
    choices = [
        f"{first} and {second}",
        f"{first} and {third}",
        f"{second} and {third}",
    ]

    answer = np.argmax(
        [
            tree.mrca(taxon_labels=[first, second]).distance_from_root(),
            tree.mrca(taxon_labels=[first, third]).distance_from_root(),
            tree.mrca(taxon_labels=[second, third]).distance_from_root(),
        ],
    )

    return question, choices, answer, [newick_string]
