import flask
from flask import jsonify, request

app = flask.Flask(__name__)


@app.route("/", methods=["Get"])
def home():
    return "Testing the early stages of the api, this works"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
