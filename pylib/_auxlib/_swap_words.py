# adapted from https://stackoverflow.com/a/70209661/17332200
def swap_words(source: str, first: str, second: str) -> str:
    res = (
        source
        .replace(first, chr(0))
        .replace(second, first)
        .replace(chr(0), second)
    )

    assert sorted(res) == sorted(source)
    return res
