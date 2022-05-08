import subprocess
import sys 
import os 

from dotenv import load_dotenv 


load_dotenv()

configs_path = os.environ.get("CONFIGS_PATH")
project_base_directory = os.environ.get("PROJECT_PATH")
author = sys.argv[1]
project_name = sys.argv[2]
shell_script = f"{os.path.join(configs_path, author, project_name)}-config.sh"


def run_shell_script():
    args = [
        "/bin/bash",
        shell_script,
        "master",
        project_base_directory,
    ]

    output_stream = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open("test-output.txt", "w") as output_file:
        output_file.write(output_stream.stdout.decode("utf-8"))


output = run_shell_script()
print("Shell script finished and saved")
