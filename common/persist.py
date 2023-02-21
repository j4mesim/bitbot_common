import msgpack


def msgpack_dumpb(d: object):
    return msgpack.dumps(d)


def msgpack_loadb(b: bytes):
    return msgpack.loads(b)
