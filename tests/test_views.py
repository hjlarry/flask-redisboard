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

