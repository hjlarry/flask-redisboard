from werkzeug import url_quote_plus

from .redisboard import module


class RedisBoardExtension:
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in self._default_config().items():
            app.config.setdefault(k, v)
        app.jinja_env.filters["quote_plus"] = url_quote_plus
        app.register_blueprint(module, url_prefix="/redisboard")

    def _default_config(self):
        return {
            "REDIS_HOST": "localhost",
            "REDIS_PORT": 6379,
            "REDIS_PASSWORD": None,
            "REDIS_UNIX_SOCKET_PATH": None,
            "REDISBOARD_SOCKET_TIMEOUT": None,
            "REDISBOARD_SOCKET_CONNECT_TIMEOUT": None,
            "REDISBOARD_SOCKET_KEEPALIVE": None,
            "REDISBOARD_SOCKET_KEEPALIVE_OPTIONS": None,
            "REDISBOARD_SLOWLOG_LEN": 100,
        }
