import datetime
import time
from uuid import uuid4

from flask import abort, current_app, session
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


def list_setter(conn, key, index, value):
    value = [item.strip() for item in value.split(",")]
    conn.lpush(key, *value)


def set_setter(conn, key, index, value):
    value = [item.strip() for item in value.split(",")]
    conn.sadd(key, *value)


VALUE_SETTERS = {
    "list": list_setter,
    "string": lambda conn, key, index, value: conn.set(key, value),
    "set": set_setter,
    "zset": lambda conn, key, score, member: conn.zadd(key, {member: float(score)}),
    "hash": lambda conn, key, index, value: conn.hset(key, index, value),
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
    # redis-py under 3.0, if not set expired, the ttl return none.
    if seconds == -1 or seconds is None:
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
    return key_details, cursor


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


def _update_config(config_constants, config_value):
    for config_part, name in config_constants:
        for k, v in config_part.items():
            config_part[k]["value"] = config_value.get(k)


def _get_redis_conn_kwargs():
    return dict(
        host=current_app.config["REDIS_HOST"],
        port=current_app.config["REDIS_PORT"],
        password=current_app.config["REDIS_PASSWORD"],
        unix_socket_path=current_app.config["REDIS_UNIX_SOCKET_PATH"],
        socket_timeout=current_app.config["REDISBOARD_SOCKET_TIMEOUT"],
        socket_connect_timeout=current_app.config["REDISBOARD_SOCKET_CONNECT_TIMEOUT"],
        socket_keepalive=current_app.config["REDISBOARD_SOCKET_KEEPALIVE"],
        socket_keepalive_options=current_app.config[
            "REDISBOARD_SOCKET_KEEPALIVE_OPTIONS"
        ],
    )


# to store the same user with same redis client
# key: a generate uuid
# value: tuple(client, last_connect_time)
user_redis_cli = {}

# while clear_number grows to a num, clear long disconnect conn
clear_number = 1


def _clear_redis_connect():
    for k, v in user_redis_cli.items():
        if time.time() - v[1] > 60 * 60:
            v[0].connection_pool.disconnect()
            del user_redis_cli[k]


def _get_current_user_redis_cli():
    if "redis_cli" in session:
        client, last_connect_time = user_redis_cli.get(
            session["redis_cli"], (None, None)
        )
        if client is None:
            client = redis.Redis(**_get_redis_conn_kwargs())
        # update last conn time
        user_redis_cli[session["redis_cli"]] = client, time.time()
    else:
        user_id = str(uuid4())
        session["redis_cli"] = user_id
        client = redis.Redis(**_get_redis_conn_kwargs())
        user_redis_cli[user_id] = client, time.time()

    global clear_number
    if clear_number % 10 == 0:
        _clear_redis_connect()
        clear_number = 0
    clear_number += 1

    return client
