import random


def shuffle_choices(choices: list[str], answer: int) -> tuple[list[str], int]:
    arg = list(range(len(choices)))
    random.shuffle(arg)
    answer = arg.index(answer)
    choices = [choices[i] for i in arg]
    return choices, answer
