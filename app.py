from flask import Flask, render_template, request, abort, redirect, url_for
import re
import redis
import datetime
from urllib import parse
from collections import OrderedDict
from werkzeug import cached_property

app = Flask(__name__)
app.jinja_env.filters["quote_plus"] = parse.quote_plus


REDISBOARD_DETAIL_TIMESTAMP_KEYS = ("last_save_time",)
REDISBOARD_DETAIL_SECONDS_KEYS = ("uptime_in_seconds",)
REDISBOARD_SLOWLOG_LEN = 10
REDISBOARD_SOCKET_TIMEOUT = None
REDISBOARD_SOCKET_CONNECT_TIMEOUT = None
REDISBOARD_SOCKET_KEEPALIVE = None
REDISBOARD_SOCKET_KEEPALIVE_OPTIONS = None
INFO_GROUPS = [
    "Server",
    "Clients",
    "Memory",
    "Persistence",
    "Stats",
    "Replication",
    "Cpu",
    "Cluster",
    "Keyspace",
    "Commandstats",
]


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
        for index, value in enumerate(conn.lrange(key, start=0, end=-1), 1)
    ]


def hash_getter(conn, key):
    return [(_decode_bytes(k), _decode_bytes(v)) for k, v in conn.hgetall(key).items()]


VALUE_GETTERS = {
    "list": list_getter,
    "string": lambda conn, key, *args: [("", _decode_bytes(conn.get(key)))],
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


def safeint(value):
    try:
        return int(value)
    except ValueError:
        return value


def _fixup_pair(pair):
    a, b = pair
    return a, safeint(b)


def _decode_bytes(value):
    if isinstance(value, bytes):
        try:
            result = value.decode()
        except UnicodeDecodeError:
            result = value
    else:
        result = value
    return result


class RedisServer:
    sampling_threshold = 1000

    @cached_property
    def connection(self):
        return redis.Redis(
            # host=hostname,
            # port=self.port,
            # password=self.password,
            # socket_timeout=REDISBOARD_SOCKET_TIMEOUT,
            # socket_connect_timeout=REDISBOARD_SOCKET_CONNECT_TIMEOUT,
            # socket_keepalive=REDISBOARD_SOCKET_KEEPALIVE,
            # socket_keepalive_options=REDISBOARD_SOCKET_KEEPALIVE_OPTIONS,
        )

    @cached_property
    def info(self):
        pipe = server.connection.pipeline()
        for part in INFO_GROUPS:
            pipe.info(part)
        results = pipe.execute()
        return dict(zip(INFO_GROUPS, results))

    @cached_property
    def databases(self):
        return [item[2:] for item in self.info["Keyspace"].keys()]

    def slowlog_len(self):
        try:
            return self.connection.slowlog_len()
        except redis.exceptions.ConnectionError:
            return 0

    def slowlog_get(self, limit=REDISBOARD_SLOWLOG_LEN):
        try:
            for slowlog in self.connection.slowlog_get(REDISBOARD_SLOWLOG_LEN):
                yield dict(
                    id=slowlog["id"],
                    ts=datetime.datetime.fromtimestamp(slowlog["start_time"]),
                    duration=slowlog["duration"],
                    command=slowlog["command"],
                )

        except redis.exceptions.ConnectionError:
            pass


server = RedisServer()


def _get_db_details(db, cursor=0, count=50):
    conn = server.connection
    conn.execute_command("SELECT", db)
    new_cursor, keys = conn.scan(cursor=cursor, count=count)
    key_details = {}
    for key in keys:
        key = key.decode()
        key_details[key] = _get_key_info(conn, key)

    return dict(keys=key_details, cursor=new_cursor)


def _get_key_details(conn, db, key):
    conn.execute_command("SELECT", db)
    details = _get_key_info(conn, key)
    details["db"] = db
    # TODO paginator for some datatype
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
        "ttl": obj_ttl,
        "refcount": refcount,
        "encoding": _decode_bytes(encoding),
        "idletime": idletime,
    }


def _get_db_summary(db):
    server.connection.execute_command("SELECT", db)
    pipe = server.connection.pipeline()

    pipe.dbsize()
    for i in range(server.sampling_threshold):
        pipe.randomkey()

    results = pipe.execute()
    size = results.pop(0)
    keys = sorted(set(results))

    pipe = server.connection.pipeline()
    for key in keys:
        pipe.execute_command("DEBUG", "OBJECT", key)
        pipe.ttl(key)

    total_memory = 0
    volatile_memory = 0
    persistent_memory = 0
    total_keys = 0
    volatile_keys = 0
    persistent_keys = 0
    results = pipe.execute()
    for key, details, ttl in zip(keys, results[::2], results[1::2]):
        if not isinstance(details, dict):
            details = dict(
                _fixup_pair(i.split(b":")) for i in details.split() if b":" in i
            )

        length = details[b"serializedlength"] + len(key)

        if ttl:
            persistent_memory += length
            persistent_keys += 1
        else:
            volatile_memory += length
            volatile_keys += 1
        total_memory += length
        total_keys += 1

    if total_keys:
        total_memory = (total_memory / total_keys) * size
    else:
        total_memory = 0

    if persistent_keys:
        persistent_memory = (persistent_memory / persistent_keys) * size
    else:
        persistent_memory = 0

    if volatile_keys:
        volatile_memory = (volatile_memory / volatile_keys) * size
    else:
        volatile_memory = 0
    return dict(
        size=size,
        total_memory=total_memory,
        volatile_memory=volatile_memory,
        persistent_memory=persistent_memory,
    )


@app.context_processor
def inject_param():
    return {"databases": server.databases}


@app.route("/")
def home():
    return redirect(url_for("info"))


@app.route("/info/")
def info():
    return render_template("serverinfo.html", info=server.info)


@app.route("/db/")
@app.route("/db/<id>/")
def db_detail(id=0):
    db_detail = _get_db_summary(id)
    cursor = request.args.get("cursor", type=int, default=0)
    db_detail.update(_get_db_details(id, cursor=cursor))
    return render_template("database.html", db_detail=db_detail, db=id)


@app.route("/db/<id>/<key>")
def key_detail(id, key):
    conn = server.connection
    key = parse.unquote_plus(key)
    key_details = _get_key_details(conn, id, key)
    return render_template("key.html", key_details=key_details)


if __name__ == "__main__":
    app.run(debug=True)
