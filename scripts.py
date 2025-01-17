from asyncio.constants import ACCEPT_RETRY_DELAY
import subprocess
import base64
import os
from datetime import datetime
import requests
import glob

from rq import Queue
from worker import conn

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

q = Queue(connection=conn)


CONTRIBUTORS_EMAIL = (
    "conradalwinho@gmail.com",
    "browndesmond30@yahoo.com",
    "desmond@gradia.net",
    "moseszeggey@yahoo.com",
    "davidyevu18@gmail.com",
    "jkwokchunkan@gmail.com",
    "regioths@gmail.com",
    "fatimatib44@gmail.com",
)


class GithubChecks:
    PENDING = "pending"
    FAILED = "failure"
    ERROR = "error"
    SUCCESS = "success"

    ACCEPTED_STATUSES = [PENDING, FAILED, ERROR, SUCCESS]

    def __init__(self, token, author: str, repo: str, sha: str):
        self.header_config = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {token}"
        }
        self.checks_url = f"https://api.github.com/repos/{author}/{repo}/statuses/{sha}"
    
    def create_status(self, status: str, context=None, description=""):
        """
        Creates a github check 
        :param status: (values accepted: pending, failed, error)
        :param context: (name of the check)
        :param description:
        :returns:
        """
        assert status in self.ACCEPTED_STATUSES, f"status needs be either of {','.join(self.ACCEPTED_STATUSES)}"
        if context is None:
            context = "test case"

        response = requests.post(self.checks_url, headers=self.header_config, json={"state": status, "context": context, "description": description})
        if response.status_code != 201:
            # TODO: Better logging here
            import pdb; pdb.set_trace()

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
        print(e)  # In V2, prob log the error


def log_output(id: str, output: str, project_name, author: str = "gradia-exchange") -> str:
    """
    Saves output to a file and returns the file path
    :param output:
    :returns:
    """
    save_directory_path = os.path.join(
        os.environ.get("LOG_OUTPUT_PATH"), author
    ) 
    os.makedirs(save_directory_path, exist_ok=True)

    file_name = os.path.join(
        save_directory_path,
        f"{project_name}-{id}-{datetime.now().strftime('%d-%m-%y-%HH:%MM:%SS')}.txt",
    )
    with open(file_name, "w") as file:
        file.write(output)

    return file_name

def run_test(owner: str, repo_name: str, branch_name: str = "master", commit_hash: str = ""):
    """
    Runs the config script, logs the output and send email notifications to contributors
    :returns:
    """
    work_path = os.environ.get("PROJECT_PATH")

    path_to_shells = os.environ.get("CONFIGS_PATH")
    scripts_path = os.path.join(path_to_shells, repo_name)
    scripts = sorted(glob.glob(f"{scripts_path}/*.sh"))
    contexts = [os.path.basename(script)[:-3].split("-")[-1] for script in scripts]


    def get_last_line(output):
        lines = output.decode("utf-8").split("\n")
        if lines[-1] == "":
            return lines[-2]
        
        return lines[-1]


    auth_token = os.environ[(f"{owner}_github_token")]
    github_checks = GithubChecks(token=auth_token, author=owner, repo=repo_name, sha=commit_hash)   # Change token to use .env tokens

    for context in contexts:
        github_checks.create_status(status=github_checks.PENDING, context=context, description="Your test is still running")
    
    dependency_scripts = ["setup", "dependency_install"]

    string_output = ""
    for index, script in enumerate(scripts):
        current_context = contexts[index]
        args = [
            "/bin/bash", 
            script,
            owner,
            "master",
            work_path
        ]
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        string_output += process.stdout.decode("utf-8")

        if process.returncode != 0:
            if (current_context == "frontend_build" and process.returncode == 254):
                pass
            else:
            # send a github error check
                github_checks.create_status(status=github_checks.FAILED, context=current_context, description="Your tests failed on GradiaCI!")
                if current_context in dependency_scripts:
                    # send failed for all the other ones
                    for context in contexts[index+1:]:
                        github_checks.create_status(status=github_checks.ERROR, context=context, description="Your tests did not complete on GradiaCI!")
                    break
                continue 

        # get the last line of the ouput and if it echo's success then send a github pass else send failed
        status = get_last_line(output=process.stdout)
        if status == "status: success":
            github_checks.create_status(status=github_checks.SUCCESS, context=current_context, description="Your tests passed on GradiaCI!")
        else:
            github_checks.create_status(status=github_checks.FAILED, context=current_context, description="Your tests failed on GradiaCI!")
        
    output_file_path = log_output(id=commit_hash, project_name=repo_name, output=string_output, author=owner)

    send_email_notifications(output_file_path)


class TestRunner:
    def __init__(self, owner: str, repo_name: str, branch_name: str = "master", commit_hash: str = "") -> None:
        self.owner = owner
        self.work_path = os.environ.get("PROJECT_PATH")
        self.repo_name = repo_name
        self.branch_name = branch_name
        self.commit_hash = commit_hash

    def start(self) -> None:
        # Queue test runner here
        print("queuing task...")
        job = q.enqueue(
            run_test,
            args=(
                self.owner,
                self.repo_name,
                self.branch_name,
                self.commit_hash,
            ),
            result_ttl=5000,
            timeout=5000,
            job_timeout="1h",
        )
        print("Job queued:", job.get_id())
