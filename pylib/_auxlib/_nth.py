import itertools as it


# adapted from https://docs.python.org/3/library/itertools.html#itertools-recipes
def nth(iterable, n, default=None):
    "Returns the nth item or a default value."
    return next(it.islice(iterable, n, None), default)
