import typing

from ._shuffle_choices import shuffle_choices


def question_equivalence_identical(
    newick_string: str,
    taxa: typing.Optional[typing.Sequence[str]] = None,
) -> tuple[str, list[str], int]:

    question = (
        "Do the two given phylogenies represent the same evolutionary history?"
    )
    choices = [
        "yes, the phylogenies are equivalent",
        "no, the phylogenies are different",
    ]

    answer = 0

    choices, answer = shuffle_choices(choices, answer)

    return question, choices, answer, [newick_string, newick_string]
