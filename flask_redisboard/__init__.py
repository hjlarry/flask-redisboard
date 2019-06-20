import os
from flask import Blueprint, send_from_directory
from jinja2 import Environment, PackageLoader
from werkzeug.urls import url_quote_plus


module = Blueprint("redisboard", __name__)


class RedisBoardExtension:
    _static_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), "static"))

    def __init__(self, app=None):
        self.app = app

        # Configure jinja for the internal templates and add url rules
        # for static data
        self.jinja_env = Environment(
            autoescape=True, loader=PackageLoader(__name__, "templates")
        )
        self.jinja_env.filters["quote_plus"] = url_quote_plus

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in self._default_config(app).items:
            app.config.setdefault(k, v)

        app.add_url_rule(
            "/_redisboard/static/<path:filename>",
            "_redisboard.static",
            self.send_static_file,
        )

        app.register_blueprint(module, url_prefix="/_redisboard/views")

    def _default_config(self, app):
        return {
            "DEBUG_TB_ENABLED": app.debug,
            "DEBUG_TB_HOSTS": (),
            "DEBUG_TB_INTERCEPT_REDIRECTS": True,
            "DEBUG_TB_PANELS": (
                "flask_debugtoolbar.panels.versions.VersionDebugPanel",
            ),
        }

    def send_static_file(self, filename):
        """Send a static file from the flask-debugtoolbar static directory."""
        return send_from_directory(self._static_dir, filename)
