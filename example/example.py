import sys

sys.path.insert(0, ".")

from flask import Flask, redirect
from flask_redisboard import RedisBoardExtension


app = Flask(__name__)
app.config["SECRET_KEY"] = "this is a key"
app.config["DEBUG"] = True

board = RedisBoardExtension(app)


@app.route("/")
def index():
    return redirect("/redisboard/dashboard", code=302)


if __name__ == "__main__":
    app.run(port=6999)
