from flask_redisboard.redisboard import server


def test_redis_connect(app):
    with app.app_context():
        assert server.connection.ping() == True
