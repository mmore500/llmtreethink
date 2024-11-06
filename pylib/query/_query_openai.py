import os
import time
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

    retries = [100, 3]["CI" in os.environ]
    for retry in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            break

        except openai.error.RateLimitError as e:
            print(e)
            print(f"Rate limit error, retrying in {retry} minutes...")
            time.sleep(60 * retry)
    else:
        raise RuntimeError("Rate limit error, too many retries")

    # Extract the response from the LLM
    llm_answer_raw = response["choices"][0]["message"]["content"].strip()

    return score_llm_answer(prompt, choices, true_answer, llm_answer_raw)
