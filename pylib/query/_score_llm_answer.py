import datetime
import typing

import opytional as opyt

from ._parse_llm_answer import parse_llm_answer


def score_llm_answer(
    prompt: str,
    choices: list[str],
    true_answer: int,
    llm_answer_raw: typing.Optional[int],
) -> dict:
    llm_answer_parsed = parse_llm_answer(llm_answer_raw, choices)
    return {
        "prompt": prompt,
        "choices": "|".join(choices),
        "response": llm_answer_raw,
        "true answer": true_answer,
        "llm answer": llm_answer_parsed,
        "score": float(llm_answer_parsed == true_answer),
        "score - invalid as nan": opyt.apply_if_or_value(
            llm_answer_parsed,
            lambda x: float(x == true_answer),
            float("nan"),
        ),
        "timestamp": datetime.datetime.now().isoformat(),
    }
