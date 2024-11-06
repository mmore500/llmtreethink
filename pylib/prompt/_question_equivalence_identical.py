import typing


def question_equivalence_identical(
    newick_string: str,
    taxa: typing.Optional[typing.Sequence[str]] = None,
) -> tuple[str, list[str], int]:

    question = (
        f"Do the two given phylogenies represent the same tree structure?"
    )
    choices = [
        f"yes, the phylogenies are equivalent",
        f"no, the phylogenies are different",
    ]

    answer = 0

    return question, choices, answer, [newick_string, newick_string]
