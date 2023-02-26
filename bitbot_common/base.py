import collections


def unpack_dict(
    d, recursive=True, include=None, keep_empty_dicts=True, return_as_dict=False
):

    """
    Unpacking nested dictionaries into flat lists of keys, values

    Parameters
    ----------
    d: dictionary
    recursive: bool
    include: callable on dict value

    Returns
    -------
    keys: list of list of nested keys
    values: values from nested dict d.
    """
    keys = []
    values = []
    for k, v in d.items():
        if isinstance(v, collections.abc.Mapping) and keep_empty_dicts and not len(v):
            keys.append([k])
            values.append(v)
        elif isinstance(v, collections.abc.Mapping) and recursive:
            for k_tuple, v_ in zip(
                *unpack_dict(d[k], recursive, include, keep_empty_dicts)
            ):
                keys.append([k] + list(k_tuple))
                values.append(v_)
        elif include is None or include(v):
            keys.append([k])
            values.append(v)
    keys = list(map(tuple, keys))
    return dict(zip(keys, values)) if return_as_dict else (keys, values)


def repack_dict(keys, values, d=None):
    """Repacking nested dictionaries into flat lists of keys, values"""
    d = {} if d is None else d
    keys_dict, values_dict = {}, {}
    for k, v in zip(keys, values):
        k = list(k if isinstance(k, (tuple, list)) else [k])
        if len(k) > 1:
            keys_dict.setdefault(k[0], []).append(k[1:])
            values_dict.setdefault(k[0], []).append(v)
    for k0 in keys_dict:
        d[k0] = repack_dict(keys_dict[k0], values_dict[k0], d.get(k0, {}))
    d.update(dict(((k[0], v) for k, v in zip(keys, values) if len(k) == 1)))
    return d



def rezip(iterable, n=2, strict=True):
    iterable = tuple(iterable)
    if len(iterable):
        return zip(*iterable, strict=strict)
    if n:
        return [()] * n
    raise ValueError
