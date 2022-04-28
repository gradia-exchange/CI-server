import subprocess
from subprocess import PIPE


def run_shell_script():
    args = [
        "/bin/bash",
        "/home/user/.configs/gradia-lab-sample-config.sh",
        "test-branch",
        "/home/user/development/business/Gradia Limited/",
    ]

    output_stream = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open("test-output.txt", "w") as output_file:
        output_file.write(output_stream.stdout.decode("utf-8"))


output = run_shell_script()
print("Shell script finished and saved")
