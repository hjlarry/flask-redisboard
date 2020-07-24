def test_home_redirect(client):
    rv = client.get("/")
    assert rv.status_code == 302


def test_blueprint_index_redirect(client):
    rv = client.get("/redisboard/")
    assert rv.status_code == 302


def test_dashboard(client):
    rv = client.get("/redisboard/dashboard/")
    assert rv.status_code == 200
    assert b"Total Memory" in rv.data


def test_dashboard_api(client):
    rv = client.get("/redisboard/dashboard_api/")
    assert rv.status_code == 200
    res = rv.get_json()
    assert res["code"] == 0
    assert "memory" in res["data"]


def test_info(client):
    rv = client.get("/redisboard/info/")
    assert rv.status_code == 200
    assert b"SlowlogTable" in rv.data


def test_config(client):
    rv = client.get("/redisboard/config/")
    assert rv.status_code == 200
    assert b"LATENCY MONITOR" in rv.data

    rv = client.post("/redisboard/config/", data=dict(name="maxclients", value="9999"))
    assert rv.get_json()["code"] == 0


def test_db(client):
    rv = client.get("/redisboard/db/")
    assert rv.status_code == 200
    assert b"Separate multiple" in rv.data

    # with cursor should response json
    rv = client.get("/redisboard/db/?cursor=1")
    res = rv.get_json()
    assert res["code"] == 0
    assert "/redisboard/db/" in res["data"]


def test_add_key(client):
    str_test = dict(type="string", keyname="a", value="astring")
    list_test = dict(type="list", keyname="b", value="1,3335,5")
    hash_test = dict(type="hash", keyname="c", index="hashkey", value="hashvalue")
    set_test = dict(type="set", keyname="d", value="1919,3,1919")
    zset_test = dict(type="zset", keyname="e", index="1233", value="zsetvalue")

    rv = client.post("/redisboard/db/2/addkey", data=str_test)
    assert rv.status_code == 302

    rv = client.post("/redisboard/db/2/addkey", data=list_test)
    assert rv.status_code == 302

    rv = client.post("/redisboard/db/2/addkey", data=hash_test)
    assert rv.status_code == 302

    rv = client.post("/redisboard/db/2/addkey", data=set_test)
    assert rv.status_code == 302

    rv = client.post("/redisboard/db/2/addkey", data=zset_test)
    assert rv.status_code == 302


def test_get_key(client):
    rv = client.get("/redisboard/db/2/a")
    assert rv.status_code == 200
    assert b"astring" in rv.data

    rv = client.get("/redisboard/db/2/b")
    assert rv.status_code == 200
    assert b"3335" in rv.data

    rv = client.get("/redisboard/db/2/c")
    assert rv.status_code == 200
    assert b"hashvalue" in rv.data

    rv = client.get("/redisboard/db/2/d")
    assert rv.status_code == 200
    assert b"1919" in rv.data

    rv = client.get("/redisboard/db/2/e")
    assert rv.status_code == 200
    assert b"zsetvalue" in rv.data
    assert b"1233" in rv.data
