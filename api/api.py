import flask
from flask import Flask, jsonify, request

app = flask.Flask(__name__)


@app.route("/", methods=["Get"])
def home():
    return "Testing the early stages of the api, this works, changes made"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
