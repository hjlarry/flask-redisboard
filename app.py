from flask import Flask, jsonify
from redis import Redis

app = Flask(__name__)
conn = Redis()


@app.route("/")
def home():
    return jsonify(conn.info())


if __name__ == "__main__":
    app.run()
