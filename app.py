import subprocess
from subprocess import PIPE
import os
from pathlib import Path

from .script import ScriptExecutionThread

from flask import Flask, request


app = Flask(__name__)

PORT = "8000"

DEBUG = False  # Change to True during dev

BASE_WORK_DIR = (
    str(Path.home()) if DEBUG else "/var/www/sites/"
)  # pythonanywhere directory (we are defaulting to use that 🤨)


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

    execution_thread = ScriptExecutionThread(work_path=BASE_WORK_DIR, repo_name=repo_name)
    execution_thread.start()

    return {"status": "ok"}


if __name__ == "__main__":
    app.run(port=PORT)
