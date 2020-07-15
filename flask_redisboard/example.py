import click
from flask import Flask, redirect
from flask_redisboard import RedisBoardExtension


app = Flask(__name__)
app.config["SECRET_KEY"] = "this is a key"
app.config["DEBUG"] = True

board = RedisBoardExtension(app)


@app.route("/")
def index():
    return redirect("/redisboard/dashboard", code=302)


@click.command()
@click.option("--port", default=6999, help="example site port")
def main(port):
    click.echo(f"redisboard example is run on port: {port}")
    app.run(port=port)
