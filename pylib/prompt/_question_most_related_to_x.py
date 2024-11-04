import random
import typing

import dendropy as dp
import numpy as np


def question_most_related_to_x(
    newick_string: str,
    taxa: typing.Optional[typing.Sequence[str]] = None,
) -> tuple[str, list[str], int]:
    tree = dp.Tree.get(data=newick_string, schema="newick")
    if taxa is None:
        taxa = random.sample(
            [x.taxon.label for x in tree.leaf_nodes()],
            3,
        )

    target, first, second = taxa
    question = f"Which among {first} and {second} are most closely related to {target}?"
    choices = [
        f"{first}",
        f"{second}",
        "neither",
    ]

    dfr1 = tree.mrca(taxon_labels=[target, first]).distance_from_root()
    dfr2 = tree.mrca(taxon_labels=[target, second]).distance_from_root()

    answer = np.argmax(
        [
            dfr1,
            dfr2,
            (dfr1 == dfr2) * (dfr1 + dfr2),
        ],
    )

    return question, choices, answer
