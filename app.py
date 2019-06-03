from flask import Flask, render_template
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


def prettify(key, value):
    if key in REDISBOARD_DETAIL_SECONDS_KEYS:
        return key, datetime.timedelta(seconds=value)
    elif key in REDISBOARD_DETAIL_TIMESTAMP_KEYS:
        return key, datetime.fromtimestamp(value)
    else:
        return key, value


class RedisServer:
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


@app.route("/")
def home():
    server = RedisServer()
    context = {
        "databases": None,
        "key_details": None,
        "original": None,
        "stats": server.stats,
        "app_label": "redisboard",
    }
    return render_template("redis.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
