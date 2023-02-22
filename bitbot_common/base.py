def rezip(iterable, n=2, strict=True):
    iterable = tuple(iterable)
    if len(iterable):
        return zip(*iterable, strict=strict)
    if n:
        return [()] * n
    raise ValueError
