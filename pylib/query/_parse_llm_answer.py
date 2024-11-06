import typing
import warnings


def parse_llm_answer(
    llm_answer_raw: str,
    choices: list[str],
) -> typing.Optional[int]:
    if not llm_answer_raw.isnumeric():
        answers = []
        for llm_answer_int, choice in enumerate(choices):
            if choice in llm_answer_raw or llm_answer_raw in choice:
                answers.append(llm_answer_int)

        if len(answers) == 1:
            return answers[0]
        else:
            warnings.warn(
                f"The LLM provided an invalid answer {llm_answer_raw}.",
            )
            return None
    else:
        llm_answer_int = int(llm_answer_raw)
        if not 0 <= llm_answer_int < len(choices):
            warnings.warn(
                f"The LLM provided an invalid answer {llm_answer_raw}.",
            )
            return None

        return llm_answer_int
