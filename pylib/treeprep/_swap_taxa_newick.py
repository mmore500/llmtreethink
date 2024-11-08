import random

from .._auxlib._swap_words import swap_words


def swap_taxa_newick(newick_str: str) -> str:
    assert ":" not in newick_str

    taxa = (
        newick_str.replace("(", " ")
        .replace(")", " ")
        .replace(",", " ")
        .replace(";", "")
        .replace("[&]", "")
        .replace("[&R]", "")
        .split()
    )
    assert len(taxa) > 1
    for _ in range(10000):
        a, b = random.sample(taxa, 2)
        if not any(
            x in newick_str
            for x in [
                f"{a},{b}",
                f"{b},{a}",
                f"{a}(",
                f"{b}(",
            ]
        ):
            return swap_words(newick_str, a, b)
    else:
        assert False
