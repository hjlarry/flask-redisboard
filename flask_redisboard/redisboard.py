from datetime import datetime

from collections.abc import Iterable

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
    get_template_attribute,
)

from werkzeug import cached_property, url_quote_plus, url_unquote_plus

from .utils import (
    _get_db_details,
    _get_key_details,
    _get_key_info,
    VALUE_SETTERS,
    _decode_bytes,
    _update_config,
    _get_redis_conn_kwargs,
    _get_current_user_redis_cli,
)
from .constant import BADGE_CLASS, INFO_GROUPS, CONFIG

module = Blueprint(
    "redisboard",
    __name__,
    template_folder="templates/redisboard",
    static_folder="static",
)


class RedisServer:
    @cached_property
    def connection(self):
        return redis.Redis(**_get_redis_conn_kwargs())

    @property
    def info(self):
        pipe = self.connection.pipeline()
        for part in INFO_GROUPS:
            pipe.info(part)
        results = pipe.execute()
        return dict(zip(INFO_GROUPS, results))

    @cached_property
    def config_file(self):
        return self.connection.info("Server").get("config_file")

    @property
    def keyspace(self):
        return self.connection.info("Keyspace")

    @property
    def memory(self):
        return self.connection.info("Memory")

    @property
    def clients(self):
        return self.connection.info("Clients")

    @property
    def stats(self):
        return self.connection.info("Stats")

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
                    ts=datetime.fromtimestamp(slowlog["start_time"]),
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
    return redirect(url_for("redisboard.dashboard"))


@module.route("/dashboard/")
def dashboard():
    total_keys = 0
    for k, v in server.keyspace.items():
        total_keys += v["keys"]
    used_memory = server.memory.get("used_memory_human")
    connected_clients = server.clients.get("connected_clients")
    return render_template(
        "dashboard.html",
        total_keys=total_keys,
        used_memory=used_memory,
        connected_clients=connected_clients,
    )


@module.route("/dashboard_api/")
def dashboard_api():
    cmd_per_sec = server.stats.get("instantaneous_ops_per_sec")
    memory = server.memory.get("used_memory") / 1024 / 1024
    network_input = server.stats.get("instantaneous_input_kbps")
    network_output = server.stats.get("instantaneous_output_kbps")
    data = {
        "cmd_per_sec": cmd_per_sec,
        "memory": memory,
        "network_input": network_input,
        "network_output": network_output,
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    return jsonify({"code": 0, "data": data})


@module.route("/info/")
def info():
    return render_template(
        "serverinfo.html",
        basic_info=server.info,
        keyspace=server.keyspace,
        cmdstats=server.commandstats,
        slowlog=server.slowlog_get(),
    )


@module.route("/config/", methods=["GET", "POST"])
def config():
    conn = server.connection
    if request.method == "POST":
        value = ""
        if "value" in request.form:
            value = request.form.get("value")
        elif "value[]" in request.form:
            value = "".join(request.form.getlist("value[]"))
        try:
            conn.config_set(request.form.get("name"), value)
        except Exception as e:
            return jsonify({"code": 999, "error": str(e)})
        return jsonify({"code": 0})
    config_value = conn.config_get()
    _update_config(CONFIG, config_value)
    return render_template("config.html", config_file=server.config_file, config=CONFIG)


@module.route("/db/")
@module.route("/db/<db>/")
def db_detail(db=0):
    db_summary = server.keyspace.get(f"db{db}", dict())
    cursor = request.args.get("cursor", type=int, default=0)
    keypattern = request.args.get("keypattern", default="")
    # when search, use bigger paginate number
    count = 1000 if keypattern else 30
    key_details, next_cursor = _get_db_details(
        server.connection, db, cursor=cursor, keypattern=keypattern, count=count
    )
    if cursor == 0:
        # render index page
        return render_template(
            "database.html",
            db_summary=db_summary,
            key_details=key_details,
            cursor=next_cursor,
            db=db,
            badge_class=BADGE_CLASS,
            keypattern=keypattern,
        )
    macro = get_template_attribute("macros.html", "render_key_details")
    html = macro(key_details, db, BADGE_CLASS)
    url = ""
    if next_cursor != 0:
        url = url_for(
            "redisboard.db_detail", db=db, cursor=next_cursor, keypattern=keypattern
        )
    return jsonify({"code": 0, "html": html, "data": url})


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
    return jsonify({"code": 0, "data": url_for("redisboard.db_detail", db=db)})


@module.route("/db/<db>/key/<key>/del", methods=["DELETE"])
def key_delete(db, key):
    conn = server.connection
    conn.execute_command("SELECT", db)
    key = url_unquote_plus(key)
    conn.delete(key)
    return jsonify({"code": 0, "data": url_for("redisboard.db_detail", db=db)})


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
    index = request.form.get("name", type=int)
    conn.lset(ori_key, index, request.form.get("value"))
    return jsonify({"code": 0})


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
    conn.hset(ori_key, request.form.get("name"), request.form.get("value"))
    return jsonify({"code": 0})


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
    maps = {request.form.get("name"): request.form.get("value", type=float)}
    conn.zadd(ori_key, maps)
    return jsonify({"code": 0})


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


@module.route("/command/", methods=["GET", "POST"])
def command():
    client = _get_current_user_redis_cli()
    if request.method == "GET":
        return render_template("command.html")
    command = request.form.get("command")
    result = client.execute_command(command)
    if isinstance(result, bytes):
        result = result.decode()
    elif isinstance(result, Iterable):
        result = [r.decode() for r in result]
    return jsonify({"code": 0, "data": result})

