import datetime

from flask import abort
import redis


def zset_getter(conn, key):
    result = conn.zrange(key, start=0, end=-1, withscores=True)
    result = [(_decode_bytes(item[0]), item[1]) for item in result]
    return result


def set_getter(conn, key):
    return ",   ".join([_decode_bytes(value) for value in conn.smembers(key)])


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


def _get_db_details(conn, db, cursor=0, keypattern=None, count=20):
    conn.execute_command("SELECT", db)
    keypattern = f"*{keypattern}*" if keypattern else None
    cursor, keys = conn.scan(cursor=cursor, match=keypattern, count=count)
    key_details = [_get_key_info(conn, key.decode()) for key in keys]
    return dict(key_details=key_details, cursor=cursor)


def _get_key_details(conn, db, key):
    conn.execute_command("SELECT", db)
    details = _get_key_info(conn, key)
    details["db"] = db
    details["data"] = VALUE_GETTERS[details["type"]](conn, key)
    return details


def _get_key_info(conn, key):
    obj_type = conn.type(key)
    if obj_type == b"none":
        abort(404)
    pipe = conn.pipeline()
    try:
        pipe.object("REFCOUNT", key)
        pipe.object("ENCODING", key)
        pipe.object("IDLETIME", key)
        LENGTH_GETTERS[obj_type](pipe, key)
        pipe.ttl(key)

        refcount, encoding, idletime, obj_length, obj_ttl = pipe.execute()
    except redis.exceptions.ResponseError as exc:
        return {
            "type": obj_type,
            "name": key,
            "length": "n/a",
            "error": str(exc),
            "ttl": "n/a",
            "refcount": "n/a",
            "encoding": "n/a",
            "idletime": "n/a",
        }
    return {
        "type": _decode_bytes(obj_type),
        "name": key,
        "length": obj_length,
        "ttl": ttl_formatter(obj_ttl),
        "refcount": refcount,
        "encoding": _decode_bytes(encoding),
        "idletime": idletime,
    }
