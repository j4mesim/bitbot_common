import msgpack
import json
import numbers
import numpy as np
from _utils.base import unpack_dict, repack_dict


def _son_dump(d):
    if isinstance(d, (tuple, list, set)):
        return tuple(d)
    keys, values = unpack_dict(d)
    for n, v in enumerate(values):
        if np.ndarray is not None and isinstance(v, np.ndarray):  # Json can't represent np.ndarray.
            values[n] = v.tolist()
        elif isinstance(v, numbers.Integral):
            values[n] = int(v)
        elif isinstance(v, numbers.Real):  # JSON can't do np.float32, pathetic.
            values[n] = float(v)
    return repack_dict(keys, values)


def msgpack_dumpb(d: object):
    return msgpack.dumps(d)


def msgpack_loadb(b: bytes):
    return msgpack.loads(b)


def json_load(fp):
    return json.load(open(fp, 'r'))


def json_dumps(d):
    """eyeball friendly json that accepts numpy arrays"""
    return json.dumps(_son_dump(d), sort_keys=True, indent=4, separators=(',', ': '))
