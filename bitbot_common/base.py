def rezip(iterable, n=2, strict=True):
    iterable = tuple(iterable)
    if len(iterable):
        return (zip_strict if strict else zip)(*iterable)
    if n:
        return [()] * n
    raise ValueError
