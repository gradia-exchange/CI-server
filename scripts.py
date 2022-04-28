import subprocess
from threading import Thread
import base64
import os
from datetime import datetime

from dotenv import load_dotenv

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)


load_dotenv()


CONTRIBUTORS_EMAIL = (
    "conradalwinho@gmail.com",
    "browndesmond30@yahoo.com",
    "desmond@gradia.net",
    "moseszeggey@yahoo.com",
    "davidyevu18@gmail.com",
    "jkwokchunkan@gmail.com",
    "regioths@gmail.com"
)


def send_email_notifications(output_file_path: str) -> None:
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

    sender_instance = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    try:
        return sender_instance.send(message)
    except Exception as e:
        print(e)  # .message)  # In V2, prob log the error


def log_output(id, output: str) -> str:
    """
    Saves output to a file and returns the file path
    :param output:
    :returns:
    """
    save_directory_path = os.environ.get("LOG_OUTPUT_PATH")
    if not os.path.exists(save_directory_path):
        os.mkdir(save_directory_path)

    file_name = os.path.join(
        save_directory_path, f"test-output-{datetime.now().strftime('%d-%m-%y-%HH:%MM:%SS')}-{id}.txt"
    )
    with open(file_name, "w") as file:
        file.write(output)

    return file_name


class ScriptExecutionThread(Thread):
    def __init__(self, repo_name: str, branch_name: str = "master", commit_hash: str = "") -> None:
        Thread.__init__(self)
        self.work_path = os.environ.get("PROJECT_PATH")
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.commit_hash = commit_hash

    def run(self) -> None:
        """
        Runs the config script, logs the output and send email notifications to contributors
        :returns:
        """
        path_to_shells = os.environ.get("CONFIGS_PATH")
        shell_script_path = os.path.join(path_to_shells, f"{self.repo_name}-config.sh")

        args = ["/bin/bash", shell_script_path, self.branch_name, self.work_path]

        p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        string_output = p.stdout.decode("utf-8")
        output_file_path = log_output(id=self.commit_hash, output=string_output)

        send_email_notifications(output_file_path)
