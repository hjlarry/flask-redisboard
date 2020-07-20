import click
from flask import Flask, redirect, Response
from flask_redisboard import RedisBoardExtension


app = Flask(__name__)
app.config["SECRET_KEY"] = "this is a key"
app.config["DEBUG"] = True

board = RedisBoardExtension(app)


@app.route("/")
def index() -> Response:
    return redirect("/redisboard/dashboard", code=302)


@click.command()
@click.option("--port", default=6999, help="example site port")
def main(port: int) -> None:
    click.echo(f"redisboard example is run on port: {port}")
    app.run(port=port)
