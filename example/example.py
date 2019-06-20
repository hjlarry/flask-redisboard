import sys

sys.path.insert(0, ".")

from flask import Flask, render_template, redirect, url_for
from flask_redisboard import RedisBoardExtension


app = Flask(__name__)
app.config["SECRET_KEY"] = "asd"
app.config["DEBUG"] = True

board = RedisBoardExtension(app)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
