import typing


def question_equivalence_identical(
    newick_string: str,
    taxa: typing.Optional[typing.Sequence[str]] = None,
) -> tuple[str, list[str], int]:

    question = (
        "Do the two given phylogenies represent the same tree structure?"
    )
    choices = [
        "yes, the phylogenies are equivalent",
        "no, the phylogenies are different",
    ]

    answer = 0

    return question, choices, answer, [newick_string, newick_string]
