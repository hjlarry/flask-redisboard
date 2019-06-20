import os
from flask import Blueprint, send_from_directory
from jinja2 import Environment, PackageLoader
from werkzeug.urls import url_quote_plus


from .redisboard import module


class RedisBoardExtension:
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in self._default_config(app).items():
            app.config.setdefault(k, v)
        app.jinja_env.filters["quote_plus"] = url_quote_plus
        app.register_blueprint(module, url_prefix="/redisboard")

    def _default_config(self, app):
        return {
            "DEBUG_TB_ENABLED": app.debug,
            "DEBUG_TB_HOSTS": (),
            "DEBUG_TB_INTERCEPT_REDIRECTS": True,
            "DEBUG_TB_PANELS": (
                "flask_debugtoolbar.panels.versions.VersionDebugPanel",
            ),
        }

