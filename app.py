import os
from pathlib import Path

import git as gitMod
from git import Repo

from flask import Flask, request


app = Flask(__name__)

PORT = "8000"

DEBUG = True

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


"""
List of things to do upon push notification:
    - pull updated stream
    - activate virtualenv
    - run test
    - send email to contributors if there are any failures (i.e for V1. After V1 prob send test summary whether pass or fail)
"""


# TODO: Fill out this function. (Does nothing now.)
def send_emails(contributor_emails=[]):
    """
    Sends emails to contributors
    :param contributor_emails:
    :returns:
    """
    pass


# TODO: Fill out this function. (Dummy now)
def run_tests():
    """
    Runs tests and pipe the output into a file
    :returns:
    """
    # Run some tests
    # Inspect the test and provide summary on:
    #  - number of test cases
    #  - number passes
    #  - number failures
    # returns this information
    pass


@app.route("/payload/", methods=["POST"])
def handle_webhooks():
    """
    This is our webhooks handler. Current Implementation only supports push events
    :returns:
    """
    clone_url = request.json["repository"]["clone_url"]
    repo_name = request.json["repository"]["name"]

    project_directory = os.path.join(BASE_WORK_DIR, repo_name)

    if not os.path.exists(project_directory):
        Repo.clone_from(clone_url, project_directory)

    git = gitMod.cmd.Git(project_directory)
    git.pull()

    return {"status": "ok"}


if __name__ == "__main__":
    app.run(port=PORT)
