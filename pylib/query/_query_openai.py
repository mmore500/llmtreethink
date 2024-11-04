import typing

import openai

from ._score_llm_answer import score_llm_answer


def query_openai(
    prompt: str,
    choices: list[str],
    true_answer: int,
    model: str = "gpt-4",
) -> tuple[typing.Optional[int], str]:

    assert 0 <= true_answer < len(choices)

    response = openai.ChatCompletion.create(
        model=model,  # Specify your desired model
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract the response from the LLM
    llm_answer_raw = response["choices"][0]["message"]["content"].strip()

    return score_llm_answer(prompt, choices, true_answer, llm_answer_raw)
