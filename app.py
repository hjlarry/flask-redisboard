from flask import Flask, render_template, request, abort
import re
import redis
import datetime
from collections import OrderedDict
from werkzeug import cached_property

app = Flask(__name__)


REDISBOARD_DETAIL_FILTERS = [
    re.compile(name)
    for name in (
        "aof_enabled",
        "bgrewriteaof_in_progress",
        "bgsave_in_progress",
        "changes_since_last_save",
        "db.*",
        "last_save_time",
        "multiplexing_api",
        "total_commands_processed",
        "total_connections_received",
        "uptime_in_days",
        "uptime_in_seconds",
        "vm_enabled",
        "redis_version",
    )
]
REDISBOARD_DETAIL_TIMESTAMP_KEYS = ("last_save_time",)
REDISBOARD_DETAIL_SECONDS_KEYS = ("uptime_in_seconds",)
REDISBOARD_SLOWLOG_LEN = 10
REDISBOARD_SOCKET_TIMEOUT = None
REDISBOARD_SOCKET_CONNECT_TIMEOUT = None
REDISBOARD_SOCKET_KEEPALIVE = None
REDISBOARD_SOCKET_KEEPALIVE_OPTIONS = None


VALUE_GETTERS = {
    "list": lambda conn, key, start=0, end=-1: [
        (pos + start, val) for (pos, val) in enumerate(conn.lrange(key, start, end))
    ],
    "string": lambda conn, key, *args: [("string", conn.get(key))],
    "set": lambda conn, key, *args: list(enumerate(conn.smembers(key))),
    "zset": lambda conn, key, start=0, end=-1: [
        (pos + start, val) for (pos, val) in enumerate(conn.zrange(key, start, end))
    ],
    "hash": lambda conn, key, *args: conn.hgetall(key).items(),
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
        return value.decode("utf8")
    else:
        return value


def prettify(key, value):
    if key in REDISBOARD_DETAIL_SECONDS_KEYS:
        return key, datetime.timedelta(seconds=value)
    elif key in REDISBOARD_DETAIL_TIMESTAMP_KEYS:
        return key, datetime.fromtimestamp(value)
    else:
        return key, value


class RedisServer:
    sampling_threshold = 1000
    sampling_size = 200

    @cached_property
    def connection(self):
        # if self.hostname.startswith("/"):
        #     unix_socket_path = self.hostname
        #     hostname = None
        # else:
        #     hostname = self.hostname
        #     unix_socket_path = None
        return redis.Redis(
            # host=hostname,
            # port=self.port,
            # password=self.password,
            # unix_socket_path=unix_socket_path,
            # socket_timeout=REDISBOARD_SOCKET_TIMEOUT,
            # socket_connect_timeout=REDISBOARD_SOCKET_CONNECT_TIMEOUT,
            # socket_keepalive=REDISBOARD_SOCKET_KEEPALIVE,
            # socket_keepalive_options=REDISBOARD_SOCKET_KEEPALIVE_OPTIONS,
        )

    @cached_property
    def stats(self):
        try:
            conn = self.connection
            info = conn.info()
            slowlog = conn.slowlog_get()
            slowlog_len = conn.slowlog_len()
            return {
                "status": "UP",
                "details": info,
                "memory": f"{info['used_memory_human']} (peak: {info.get('used_memory_peak_human', 'n/a')})",
                "clients": info["connected_clients"],
                "brief_details": OrderedDict(
                    prettify(k, v)
                    for name in REDISBOARD_DETAIL_FILTERS
                    for k, v in info.items()
                    if name.match(k)
                ),
                "slowlog": slowlog,
                "slowlog_len": slowlog_len,
            }
        except redis.exceptions.ConnectionError:
            return {
                "status": "DOWN",
                "clients": "n/a",
                "memory": "n/a",
                "details": {},
                "brief_details": {},
                "slowlog": [],
                "slowlog_len": 0,
            }
        except redis.exceptions.ResponseError as exc:
            return {
                "status": f"ERROR: {exc.args}",
                "clients": "n/a",
                "memory": "n/a",
                "details": {},
                "brief_details": {},
                "slowlog": [],
                "slowlog_len": 0,
            }

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


def _get_db_details(server, db):
    conn = server.connection
    conn.execute_command("SELECT", db)
    size = conn.dbsize()

    key_details = {}
    if size > server.sampling_threshold:
        sampling = True
        pipe = conn.pipeline()
        for _ in range(server.sampling_size):
            pipe.randomkey()

        for key in set(pipe.execute()):
            key_details[key] = _get_key_info(conn, key)

    else:
        sampling = False
        for key in conn.keys():
            key_details[key] = _get_key_info(conn, key)

    return dict(keys=key_details, sampling=sampling)


def _get_key_details(conn, db, key, page):
    conn.execute_command("SELECT", db)
    details = _get_key_info(conn, key)
    details["db"] = db
    if details["type"] in ("list", "zset"):
        # TODO paginator
        details["data"] = None
    else:
        details["data"] = VALUE_GETTERS[details["type"]](conn, key)

    return details


def _get_key_info(conn, key):
    try:
        obj_type = conn.type(key)
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
    except redis.exceptions.ResponseError as exc:
        return {
            "type": "n/a",
            "length": "n/a",
            "name": key,
            "error": str(exc),
            "ttl": "n/a",
            "refcount": "n/a",
            "encoding": "n/a",
            "idletime": "n/a",
        }


def _get_db_summary(server, db):
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


@app.route("/")
def home():
    stats = server.stats
    conn = server.connection
    database_details = OrderedDict()
    key_details = None

    if stats["status"] == "UP":
        key = request.args.get("key", None)
        if key:
            db = request.args.get("db", 0)
            page = request.args.get("page", 1)
            key_details = _get_key_details(conn, db, key, page)
        else:
            databases = sorted(
                name[2:] for name in conn.info() if name.startswith("db")
            )
            total_size = 0
            for db in databases:
                database_details[db] = summary = _get_db_summary(server, db)
                total_size += summary["size"]
            if total_size < server.sampling_threshold:
                for db in databases:
                    database_details[db].update(
                        _get_db_details(server, db), active=True
                    )
            elif "db" in request.GET:
                db = request.GET["db"]
                if db in database_details:
                    database_details[db].update(
                        _get_db_details(server, db), active=True
                    )
                else:
                    abort(404)
    context = {
        "databases": database_details,
        "key_details": key_details,
        "stats": stats,
    }
    return render_template("redis.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
