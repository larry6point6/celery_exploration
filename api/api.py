from celery.result import AsyncResult
from flask import Flask, jsonify, make_response, request

from celery_app import add_task

app = Flask(__name__)


# @app.route("/", methods=["GET"])
# def home():
#     return "Testing the early stages of the api, this works, changes made"


@app.route("/add", methods=["GET", "POST"])
def add():
    # Json body
    if request.is_json:
        data = request.get_json()
        a = int(data["a"])
        b = int(data["b"])
    else:  # Querystring
        a = request.args.get("a", type=int)
        b = request.args.get("b", type=int)

    result_task = add_task.apply_async(args=(a, b))
    return make_response(jsonify({"job_id": result_task.task_id}))


@app.route("/task/<job_id>", methods=["GET"])
def check_task_status(job_id):
    task = add_task.AsyncResult(job_id)
    output = {
        "job_id": task.id,
        "state": task.state,
    }
    if task.state == "SUCCESS":
        output = {"result": task.result}
        return jsonify(output)
    else:
        output = {"result": None}

    return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
