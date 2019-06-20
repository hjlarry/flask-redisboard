from flask import Flask, render_template, request, abort, redirect, url_for, jsonify
import re
import redis
import datetime
from urllib import parse
from collections import OrderedDict
from werkzeug import cached_property


from flask_redisboard import module
from flask_redisboard.config import INFO_GROUPS, REDISBOARD_SLOWLOG_LEN, BADGE_CLASS
from flask_redisboard.utils import (
    VALUE_GETTERS,
    LENGTH_GETTERS,
    _decode_bytes,
    ttl_formatter,
)


class RedisServer:
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
conn = server.connection


def _get_db_details(db, cursor=0, keypattern=None, count=20):
    conn = server.connection
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


@module.context_processor
def inject_param():
    return {"databases": server.databases}


@module.errorhandler(Exception)
def handle_exception(error):
    return jsonify({"code": 999, "error": str(error)})


@module.route("/")
def home():
    return redirect(url_for("info"))


@module.route("/info/")
def info():
    return render_template("serverinfo.html", info=server.info)


@module.route("/db/")
@module.route("/db/<db>/")
def db_detail(db=0):
    # 需要复制一下，以免影响到原info中的信息
    db_detail = server.info.get("Keyspace").get(f"db{db}").copy() or dict()
    # 避免和dict.keys()重名
    db_detail["_keys"] = db_detail["keys"] if "keys" in db_detail else 0
    cursor = request.args.get("cursor", type=int, default=0)
    keypattern = request.args.get("keypattern", default="")
    # 当搜索时使用更大的分页值
    count = 1000 if keypattern else 20
    db_detail.update(
        _get_db_details(db, cursor=cursor, keypattern=keypattern, count=count)
    )
    return render_template(
        "database.html",
        db_detail=db_detail,
        db=db,
        count=count,
        badge_class=BADGE_CLASS,
        keypattern=keypattern,
    )


@module.route("/db/<db>/batchttl", methods=["POST"])
def batch_set_ttl(db):
    conn.execute_command("SELECT", db)
    pipe = server.connection.pipeline()
    keys = request.json.get("keys", [])
    ttl = int(request.json.get("ttl", -1))
    for key in keys:
        if ttl <= 0:
            pipe.persist(key)
        else:
            pipe.expire(key, ttl)
    pipe.execute()
    return jsonify({"code": 0, "data": url_for("db_detail", db=db)})


@module.route("/db/<db>/batchdel", methods=["POST"])
def batch_delete_keys(db):
    conn.execute_command("SELECT", db)
    keys = request.json.get("keys", [])
    conn.delete(*keys)
    return jsonify({"code": 0, "data": url_for("db_detail", db=db)})


@module.route("/api/<db>/flush", methods=["DELETE"])
def db_flush(db):
    conn.execute_command("SELECT", db)
    conn.flushdb()
    return jsonify({"data": "ok"})


@module.route("/api/<db>/key/<key>/del", methods=["DELETE"])
def key_delete(db, key):
    conn.execute_command("SELECT", db)
    key = parse.unquote_plus(key)
    conn.delete(key)
    return jsonify({"data": "ok"})


@module.route("/db/<db>/<key>/rename", methods=["POST"])
def key_rename(db, key):
    conn.execute_command("SELECT", db)
    key = parse.unquote_plus(key)
    new_name = request.form["keyname"]
    conn.rename(key, new_name)
    return jsonify(
        {
            "code": 0,
            "data": url_for("key_detail", db=db, key=parse.quote_plus(new_name)),
        }
    )


@module.route("/db/<db>/<key>/ttl", methods=["POST"])
def key_set_ttl(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    ttl = request.form.get("ttl", type=int)
    if ttl <= 0:
        conn.persist(ori_key)
    else:
        conn.expire(ori_key, ttl)
    return jsonify({"code": 0, "data": url_for("key_detail", db=db, key=key)})


@module.route("/db/<db>/<key>/list_add", methods=["POST"])
def list_add_value(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    position = request.form.get("position", type=int)
    if position == 0:
        conn.lpush(ori_key, request.form["value"])
    elif position == -1:
        conn.rpush(ori_key, request.form["value"])
    return jsonify({"code": 0, "data": url_for("key_detail", db=db, key=key)})


@module.route("/db/<db>/<key>/list_edit", methods=["POST"])
def list_edit_value(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    index = request.args.get("index", type=int, default=0)
    conn.lset(ori_key, index, request.form["value"])
    return redirect(url_for("key_detail", db=db, key=key))


@module.route("/db/<db>/<key>/list_rem", methods=["POST"])
def list_rem_value(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    count = request.form.get("count", type=int, default=1)
    conn.lrem(ori_key, count, request.form["value"])
    return jsonify({"code": 0, "data": url_for("key_detail", db=db, key=key)})


@module.route("/db/<db>/<key>/hash_add", methods=["POST"])
def hash_add_value(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    index = request.form.get("index", "")
    exists = conn.hexists(ori_key, index)
    if exists:
        return jsonify({"code": 1, "error": "can`t add value to an exist key!"})
    else:
        conn.hset(ori_key, index, request.form.get("value"))
    return jsonify({"code": 0, "data": url_for("key_detail", db=db, key=key)})


@module.route("/db/<db>/<key>/hash_edit", methods=["POST"])
def hash_edit_value(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    index = request.args.get("index")
    conn.hset(ori_key, index, request.form["value"])
    return redirect(url_for("key_detail", db=db, key=key))


@module.route("/db/<db>/<key>/hash_rem", methods=["POST"])
def hash_rem_value(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    conn.hdel(ori_key, request.form["index"])
    return jsonify({"code": 0, "data": url_for("key_detail", db=db, key=key)})


@module.route("/db/<db>/<key>/set_add", methods=["POST"])
def set_add_value(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    value = request.form.get("value", "")
    value = [item.strip() for item in value.split(",")]
    result = conn.sadd(ori_key, *value)
    # TODO response how many successed operate
    return jsonify({"code": 0, "data": url_for("key_detail", db=db, key=key)})


@module.route("/db/<db>/<key>/set_rem", methods=["POST"])
def set_rem_value(db, key):
    conn.execute_command("SELECT", db)
    ori_key = parse.unquote_plus(key)
    value = request.form.get("value", "")
    value = [item.strip() for item in value.split(",")]
    conn.srem(ori_key, *value)
    return jsonify({"code": 0, "data": url_for("key_detail", db=db, key=key)})


@module.route("/db/<db>/<key>", methods=["GET", "POST"])
def key_detail(db, key):
    conn = server.connection
    key = parse.unquote_plus(key)
    if request.method == "POST":
        conn.set(key, request.form["value"])
    key_details = _get_key_details(conn, db, key)
    return render_template(
        f"keydetail/{key_details['type']}.html", key_details=key_details, db=db
    )

