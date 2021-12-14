import flask
from flask import jsonify, request

app = flask.Flask(__name__)

# books = [
#     {
#         "id": 0,
#         "title": "A Fire Upon the Deep",
#         "author": "Vernor Vinge",
#         "first_sentence": "The coldsleep itself was dreamless.",
#         "year_published": "1992",
#     },
#     {
#         "id": 1,
#         "title": "The Ones Who Walk Away From Omelas",
#         "author": "Ursula K. Le Guin",
#         "first_sentence": "With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.",
#         "published": "1973",
#     },
#     {
#         "id": 2,
#         "title": "Dhalgren",
#         "author": "Samuel R. Delany",
#         "first_sentence": "to wound the autumnal city.",
#         "published": "1976",
#     },
# ]


@app.route("/", methods=["Get"])
def home():
    return "Testing the early stages of the api"


# # A route to return all of the available entries in our catalog.
# @app.route("/api/v1/resources/books/all", methods=["GET"])
# def api_all():
#     return jsonify(books)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
