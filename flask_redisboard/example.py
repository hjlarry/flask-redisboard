import click
from flask import Flask, redirect, Response, url_for
from flask_redisboard import RedisBoardExtension


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "this is a key"
    app.config["DEBUG"] = True

    board = RedisBoardExtension()
    board.init_app(app)

    @app.route("/")
    def index() -> Response:
        return redirect(url_for("redisboard.dashboard"))

    return app


@click.command()
@click.option("--host", default="127.0.0.1", help="example site host")
@click.option("--port", default=6999, help="example site port")
def main(host: str, port: int) -> None:
    click.echo(f"redisboard example site is running on: http://{host}:{port}")
    app = create_app()
    app.run(host=host, port=port)
