import subprocess
import sys
import os
import re

from dotenv import load_dotenv


load_dotenv()

configs_path = os.environ.get("CONFIGS_PATH")
project_base_directory = os.environ.get("PROJECT_PATH")
author = sys.argv[1]
project_name = sys.argv[2]
shell_script = f"{os.path.join(configs_path, project_name)}-config.sh"

def run_shell_script():
    args = [
        "/bin/bash",
        shell_script,
        author,
        "master",
        project_base_directory,
    ]

    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    context = ""
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break 
        if output:
            # check for the line and find the context
            print(output.strip())
            # print("return code:", process.returncode)
            # import pdb; pdb.set_trace()
            # context_found = re.match(r"^Context:", output.decode().strip())
            # if context_found is not None:
            #     context = output.decode().strip().lstrip("Context: ")
            #     # Send 

    rc = process.poll()

    output_stream = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open("test-output.txt", "w") as output_file:
        output_file.write(output_stream.stdout.decode("utf-8"))


output = run_shell_script()
print("Shell script finished and saved")
