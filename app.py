import os
from subprocess import PIPE
from pathlib import Path

from scripts import ScriptExecutionThread

from flask import Flask, request


app = Flask(__name__)

PORT = "8000"

DEBUG = True  # Change to True during dev


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
    repo_name = request.json["repository"]["name"]
    branch_name = request.json["ref"].split("/")[-1]
    commit_hash = request.json["after"]

    execution_thread = ScriptExecutionThread(repo_name=repo_name, branch_name=branch_name, commit_hash=commit_hash)
    execution_thread.start()

    return {"status": "ok"}


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
