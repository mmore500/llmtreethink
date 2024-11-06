def find_opening_parenthesis(source: str, start: int) -> int:
    depth = 1
    for i in range(start - 1, -1, -1):
        depth += source[i] == ")"
        depth -= source[i] == "("
        if depth == 0:
            return i

    assert False
