def test_home(client):
    rv = client.get("/")
    assert rv.status_code == 302
