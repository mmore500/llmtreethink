# adapted from https://stackoverflow.com/a/70209661/17332200
def swap_words(source: str, first: str, second: str) -> str:
    res = second.join(
        part.replace(second, first) for part in source.split(first)
    )
    assert sorted(res) == sorted(source)
    return res
