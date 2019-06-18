import datetime


def zset_getter(conn, key):
    result = conn.zrange(key, start=0, end=-1, withscores=True)
    result = [(_decode_bytes(item[0]), item[1]) for item in result]
    return result


def set_getter(conn, key):
    return [
        (index, _decode_bytes(value))
        for index, value in enumerate(conn.smembers(key), 1)
    ]


def list_getter(conn, key):
    return [
        (index, _decode_bytes(value))
        for index, value in enumerate(conn.lrange(key, start=0, end=1000))
    ]


def hash_getter(conn, key):
    return [(_decode_bytes(k), _decode_bytes(v)) for k, v in conn.hgetall(key).items()]


VALUE_GETTERS = {
    "list": list_getter,
    "string": lambda conn, key, *args: _decode_bytes(conn.get(key)),
    "set": set_getter,
    "zset": zset_getter,
    "hash": hash_getter,
    "n/a": lambda conn, key, *args: (),
}

LENGTH_GETTERS = {
    b"list": lambda conn, key: conn.llen(key),
    b"string": lambda conn, key: conn.strlen(key),
    b"set": lambda conn, key: conn.scard(key),
    b"zset": lambda conn, key: conn.zcount(key, "-inf", "+inf"),
    b"hash": lambda conn, key: conn.hlen(key),
}


def _decode_bytes(value):
    if isinstance(value, bytes):
        try:
            result = value.decode()
        except UnicodeDecodeError:
            result = value
    else:
        result = value
    return result


def ttl_formatter(seconds):
    if seconds == -1:
        return "forever"
    ttl = datetime.timedelta(seconds=seconds)
    mm, ss = divmod(ttl.seconds, 60)
    hh, mm = divmod(mm, 60)
    if ttl.days:
        return f"{ttl.days}day,{hh}hour,{mm}min,{ss}seconds"
    else:
        return f"{hh}hour,{mm}min,{ss}seconds"
