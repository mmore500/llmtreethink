import random

from .._auxlib._find_closing_parenthesis import find_closing_parenthesis
from .._auxlib._find_opening_parenthesis import find_opening_parenthesis
from .._auxlib._nth import nth


def try_rotate_phylogeny_newick(newick_str: str) -> str:
    num_commas = newick_str.count(",")
    sampled_comma = random.randrange(0, num_commas)
    comma_position = nth(
        (i for i, c in enumerate(newick_str) if c == ","),
        sampled_comma,
    )
    assert newick_str[comma_position] == ","

    i = find_closing_parenthesis(newick_str, comma_position)
    j = find_opening_parenthesis(newick_str, comma_position)

    assert newick_str[i] == ")" and newick_str[j] == "("
    res = "".join(
        [
            newick_str[: j + 1],
            newick_str[comma_position + 1 : i],
            ",",
            newick_str[j + 1 : comma_position],
            newick_str[i:],
        ],
    )

    assert sorted(res) == sorted(newick_str), (res, newick_str)
    return res


def rotate_phylogeny_newick(newick_str: str) -> str:
    for __ in range(10000):
        res = try_rotate_phylogeny_newick(newick_str)
        if res != newick_str:
            return res

    assert False
