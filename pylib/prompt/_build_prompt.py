import typing


def build_prompt(
    tree_strings: typing.Union[str, list[str]],
    question: str,
    choices: list[str],
) -> str:

    if isinstance(tree_strings, str):
        tree_strings = [tree_strings]

    tree_string = "\n\n---\n\n".join(tree_strings)

    # Combine the question and choices into a formatted prompt
    prompt = ""
    if tree_string:
        plural = "s" * (len(tree_strings) > 1)
        prompt += f"Consider the following phylogenetic tree{plural}:\n\n {tree_string}\n"
        prompt += "\n---\n\n"
    prompt += f"{question}\n"
    for idx, choice in enumerate(choices):
        prompt += f"{idx}: {choice}\n"

    prompt += f"Please choose the correct answer, responding only with the answer number {tuple(range(len(choices)))}:"

    return prompt
