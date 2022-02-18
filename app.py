import subprocess
from subprocess import PIPE
import os
from pathlib import Path
from datetime import datetime
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

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


CONTRIBUTORS_EMAIL = (
    "conradalwinho@gmail.com",
    "browndesmond30@yahoo.com",
    "desmond@gradia.net",
    "moseszeggey@yahoo.com",
    "davidyevu18@gmail.com",
    "jkwokchunkan@gmail.com",
)


def send_email_notifications(output_file_path):
    """
    Sends emails to contributors
    :param output_file_path:
    :returns:
    """
    message = Mail(
        from_email="Gradia CI Platform <info@gradia.net>",
        to_emails=CONTRIBUTORS_EMAIL,
        subject="Test running report",
        html_content="<p>This email contains an attachment of the file containing the test run logs</p>",
    )

    # Technically could has read as not byte that way no need for decoding but this to allow for attachment other file types like pds, etc
    with open(output_file_path, "rb") as file:
        data = file.read()

    encoded_file_content = base64.b64encode(data).decode()

    file_name = os.path.basename(output_file_path)

    attachment = Attachment(
        FileContent(encoded_file_content),
        FileName(file_name),
        FileType("application/txt"),
        Disposition("attachment"),
    )

    message.attachment = attachment

    sender_instance = SendGridAPIClient(
        "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"
    )  # os.environ.get("SENDGRID_API_KEY"))
    try:
        return sender_instance.send(message)
    except Exception as e:
        print(e)  # .message)  # In V2, prob log the error


def log_output(output):
    """
    Saves output to a file and returns the file path
    :param output:
    :returns:
    """
    save_directory_path = os.path.join(BASE_WORK_DIR, ".configs")
    if not os.path.exists(save_directory_path):
        os.mkdir(save_directory_path)

    file_name = f"test-output-{datetime.now().strftime('%d-%m-%y-%HH:%MM:%SS')}.txt"
    with open(file_name, "w") as file:
        file.write(output)

    return file_name


@app.route("/payload/", methods=["POST"])
def handle_webhooks():
    """
    This is our webhooks handler. Current Implementation only supports push events
    :returns:
    """
    # clone_url = request.json["repository"]["clone_url"]
    repo_name = request.json["repository"]["name"]

    config_script = os.path.join(os.getcwd(), ".configs", f"{repo_name}-config.sh")
    args = ["/bin/sh", config_script]

    p = subprocess.Popen(args, stdin=PIPE, stdout=PIPE)
    string_output = p.stdout.read().decode()

    output_path = log_output(string_output)

    send_email_notifications(output_path)

    return {"status": "ok"}


if __name__ == "__main__":
    app.run(port=PORT)
