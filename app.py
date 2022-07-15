import os 
from dotenv import load_dotenv

from flask import Flask, request, send_from_directory

from scripts import TestRunner


app = Flask(__name__)

PORT = "8080"

DEBUG = True


load_dotenv()

app.config["LOG_OUTPUT_DIRECTORY"] = os.environ["LOG_OUTPUT_PATH"]


@app.route("/")
def index():
    """
    In the future this page will basically show a UI for interaction with the test runs
    :returns:
    """
    return "Heya! It's Gradia's CI Implementation on Pythonanywhere 😃"


@app.route("/payload/", methods=["POST"])
def handle_webhooks():
    """
    This is our webhooks handler. Current Implementation only supports push events
    :returns:
    """
    # get repo name
    event = request.headers.get("X-GITHUB-EVENT")
    if event == "pull_request":
        repo_name = request.json["pull_request"]["head"]["repo"]["name"]
        branch_name = request.json["pull_request"]["head"]["ref"]
        owner = request.json["repository"]["owner"]["login"]
        commit_hash = request.json["pull_request"]["head"]["sha"]
    else:  # There prob may be other events that sends diff request data?
        repo_name = request.json["repository"]["name"]
        branch_name = request.json["ref"].split("/")[-1]
        owner = request.json["pusher"]["name"]
        commit_hash = request.json["head_commit"]["id"]

    execution_thread = TestRunner(
        owner=owner,
        repo_name=repo_name,
        branch_name=branch_name,
        commit_hash=commit_hash,
    )
    execution_thread.start()

    return {"status": "ok"}


@app.route("/media/<path:path>")
def send_media(path):
    """
    Returns test file
    :param path:
    :returns:
    """
    return send_from_directory(directory=app.config["LOG_OUTPUT_DIRECTORY"], path=path)


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)  # only is called during dev, but not called when deployed on pythonanywhere
