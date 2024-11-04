import os

import openai

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError(
        "Please set the environment variable OPENAI_API_KEY.",
    )
else:
    openai.api_key = os.environ["OPENAI_API_KEY"]
