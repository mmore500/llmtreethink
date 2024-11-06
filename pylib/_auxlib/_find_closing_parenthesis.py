def find_closing_parenthesis(source: str, start: int) -> int:
    depth = 1
    for i in range(start + 1, len(source)):
        depth += source[i] == "("
        depth -= source[i] == ")"
        if depth == 0:
            return i

    assert False
