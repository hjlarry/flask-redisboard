import datetime

import redis
from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug import cached_property, url_quote_plus, url_unquote_plus

from .utils import (
    _get_db_details,
    _get_key_details,
    _get_key_info,
    VALUE_SETTERS,
    _decode_bytes,
)
from .constant import GENERAL_CONFIG, NETWORK_CONFIG, BADGE_CLASS, INFO_GROUPS

module = Blueprint(
    "redisboard",
    __name__,
    template_folder="templates/redisboard",
    static_folder="static",
)


class RedisServer:
    @cached_property
    def connection(self):
        return redis.Redis(
            host=current_app.config["REDIS_HOST"],
            port=current_app.config["REDIS_PORT"],
            password=current_app.config["REDIS_PASSWORD"],
            unix_socket_path=current_app.config["REDIS_UNIX_SOCKET_PATH"],
            socket_timeout=current_app.config["REDISBOARD_SOCKET_TIMEOUT"],
            socket_connect_timeout=current_app.config[
                "REDISBOARD_SOCKET_CONNECT_TIMEOUT"
            ],
            socket_keepalive=current_app.config["REDISBOARD_SOCKET_KEEPALIVE"],
            socket_keepalive_options=current_app.config[
                "REDISBOARD_SOCKET_KEEPALIVE_OPTIONS"
            ],
        )

    @cached_property
    def info(self):
        pipe = self.connection.pipeline()
        for part in INFO_GROUPS:
            pipe.info(part)
        results = pipe.execute()
        return dict(zip(INFO_GROUPS, results))

    @property
    def keyspace(self):
        return self.connection.info("Keyspace")

    @property
    def commandstats(self):
        return self.connection.info("Commandstats")

    @property
    def databases(self):
        return [item[2:] for item in self.keyspace.keys()]

    def slowlog_get(self, limit=None):
        try:
            count = limit if limit else current_app.config["REDISBOARD_SLOWLOG_LEN"]
            for slowlog in self.connection.slowlog_get(count):
                yield dict(
                    id=slowlog["id"],
                    ts=datetime.datetime.fromtimestamp(slowlog["start_time"]),
                    duration=slowlog["duration"] // 1000,
                    command=_decode_bytes(slowlog["command"]),
                )

        except redis.exceptions.ConnectionError:
            pass


server = RedisServer()


@module.context_processor
def inject_param():
    return {"databases": server.databases}


@module.errorhandler(Exception)
def handle_exception(error):
    return jsonify({"code": 999, "error": str(error)})


@module.route("/")
def home():
    return redirect(url_for("redisboard.info"))


@module.route("/info/")
def info():
    return render_template(
        "serverinfo.html",
        basic_info=server.info,
        keyspace=server.keyspace,
        cmdstats=server.commandstats,
        slowlog=server.slowlog_get(),
    )


@module.route("/config/")
def config():
    conn = server.connection
    redis_config = conn.config_get()
    config_file = server.info["Server"].get("config_file")
    for k, v in GENERAL_CONFIG.items():
        GENERAL_CONFIG[k]["value"] = redis_config.get(k)
    for k, v in NETWORK_CONFIG.items():
        NETWORK_CONFIG[k]["value"] = redis_config.get(k)
    return render_template(
        "config.html",
        config_file=config_file,
        general_config=GENERAL_CONFIG,
        network_config=NETWORK_CONFIG,
    )


@module.route("/db/")
@module.route("/db/<db>/")
def db_detail(db=0):
    db_detail = server.keyspace.get(f"db{db}", dict())
    # avoid same name with dict.keys()
    db_detail["_keys"] = db_detail["keys"] if "keys" in db_detail else 0
    cursor = request.args.get("cursor", type=int, default=0)
    keypattern = request.args.get("keypattern", default="")
    # when search, use big paginate number
    count = 1000 if keypattern else 20
    db_detail.update(
        _get_db_details(
            server.connection, db, cursor=cursor, keypattern=keypattern, count=count
        )
    )
    return render_template(
        "database.html",
        db_detail=db_detail,
        db=db,
        count=count,
        badge_class=BADGE_CLASS,
        keypattern=keypattern,
    )


@module.route("/db/<db>/addkey", methods=["POST"])
def add_key(db):
    conn = server.connection
    conn.execute_command("SELECT", db)
    keyname = request.form.get("keyname")
    typex = request.form.get("type")
    index = request.form.get("index")
    value = request.form.get("value")
    set_method = VALUE_SETTERS.get(typex)
    set_method(conn, keyname, index, value)
    return redirect(url_for("redisboard.db_detail", db=db))


@module.route("/db/<db>/batchttl", methods=["POST"])
def batch_set_ttl(db):
    conn = server.connection
    conn.execute_command("SELECT", db)
    pipe = conn.pipeline()
    keys = request.json.get("keys", [])
    ttl = int(request.json.get("ttl", -1))
    for key in keys:
        if ttl <= 0:
            pipe.persist(key)
        else:
            pipe.expire(key, ttl)
    pipe.execute()
    return jsonify({"code": 0, "data": url_for("redisboard.db_detail", db=db)})


@module.route("/db/<db>/batchdel", methods=["POST"])
def batch_delete_keys(db):
    conn = server.connection
    conn.execute_command("SELECT", db)
    keys = request.json.get("keys", [])
    conn.delete(*keys)
    return jsonify({"code": 0, "data": url_for("redisboard.db_detail", db=db)})


@module.route("/db/<db>/flush", methods=["DELETE"])
def db_flush(db):
    conn = server.connection
    conn.execute_command("SELECT", db)
    conn.flushdb()
    return jsonify({"data": "ok"})


@module.route("/db/<db>/key/<key>/del", methods=["DELETE"])
def key_delete(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    key = url_unquote_plus(key)
    conn.delete(key)
    return jsonify({"data": "ok"})


@module.route("/db/<db>/<key>/rename", methods=["POST"])
def key_rename(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    key = url_unquote_plus(key)
    new_name = request.form["keyname"]
    conn.rename(key, new_name)
    return jsonify(
        {
            "code": 0,
            "data": url_for(
                "redisboard.key_detail", db=db, key=url_quote_plus(new_name)
            ),
        }
    )


@module.route("/db/<db>/<key>/ttl", methods=["POST"])
def key_set_ttl(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    ttl = request.form.get("ttl", type=int)
    if ttl <= 0:
        conn.persist(ori_key)
    else:
        conn.expire(ori_key, ttl)
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>/list_add", methods=["POST"])
def list_add_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    position = request.form.get("position", type=int)
    if position == 0:
        conn.lpush(ori_key, request.form["value"])
    elif position == -1:
        conn.rpush(ori_key, request.form["value"])
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>/list_edit", methods=["POST"])
def list_edit_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    index = request.args.get("index", type=int, default=0)
    conn.lset(ori_key, index, request.form["value"])
    return redirect(url_for("redisboard.key_detail", db=db, key=key))


@module.route("/db/<db>/<key>/list_rem", methods=["POST"])
def list_rem_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    count = request.form.get("count", type=int, default=1)
    conn.lrem(ori_key, count, request.form["value"])
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>/hash_add", methods=["POST"])
def hash_add_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    index = request.form.get("index", "")
    exists = conn.hexists(ori_key, index)
    if exists:
        return jsonify({"code": 1, "error": "can`t add value to an exist key!"})
    else:
        conn.hset(ori_key, index, request.form.get("value"))
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>/hash_edit", methods=["POST"])
def hash_edit_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    index = request.args.get("index")
    conn.hset(ori_key, index, request.form["value"])
    return redirect(url_for("redisboard.key_detail", db=db, key=key))


@module.route("/db/<db>/<key>/hash_rem", methods=["POST"])
def hash_rem_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    conn.hdel(ori_key, request.form["index"])
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>/set_add", methods=["POST"])
def set_add_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    value = request.form.get("value", "")
    value = [item.strip() for item in value.split(",")]
    result = conn.sadd(ori_key, *value)
    # TODO response how many successed operate
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>/set_rem", methods=["POST"])
def set_rem_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    value = request.form.get("value", "")
    value = [item.strip() for item in value.split(",")]
    conn.srem(ori_key, *value)
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>/zset_edit", methods=["POST"])
def zset_edit_score(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    maps = {request.args.get("member"): request.form.get("score", type=float)}
    conn.zadd(ori_key, maps)
    return redirect(url_for("redisboard.key_detail", db=db, key=key))


@module.route("/db/<db>/<key>/zset_add", methods=["POST"])
def zset_add_value(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    conn.zadd(
        ori_key, {request.form.get("member"): request.form.get("score", type=float)}
    )
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>/zset_rem", methods=["POST"])
def zset_rem_member(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    ori_key = url_unquote_plus(key)
    member = request.form.get("member", "")
    if member:
        members = [item.strip() for item in member.split(",")]
        conn.zrem(ori_key, *members)
    else:
        score_min, score_max = (
            request.form.get("min", type=float),
            request.form.get("max", type=float),
        )
        conn.zremrangebyscore(ori_key, score_min, score_max)
    return jsonify(
        {"code": 0, "data": url_for("redisboard.key_detail", db=db, key=key)}
    )


@module.route("/db/<db>/<key>", methods=["GET", "POST"])
def key_detail(db, key):
    conn = server.connection
    key = url_unquote_plus(key)
    if request.method == "POST":
        conn.set(key, request.form["value"])
    key_details = _get_key_details(conn, db, key)
    return render_template(
        f"keydetail/{key_details['type']}.html", key_details=key_details, db=db
    )


@module.route("/config", methods=["POST"])
def config_set():
    print(request.form)
    return jsonify({"code": 0, "data": "121"})

