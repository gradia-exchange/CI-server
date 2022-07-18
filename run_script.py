import subprocess
import sys
import os
import re
import glob

from dotenv import load_dotenv


load_dotenv()

configs_path = os.environ.get("CONFIGS_PATH")
project_base_directory = os.environ.get("PROJECT_PATH")
author = sys.argv[1]
project_name = sys.argv[2]


def get_last_line(output):
    lines = output.decode("utf-8").split("\n")
    if lines[-1] == "":
        return lines[-2]
    
    return lines[-1]


def run_shell_script():

    # Get all the scripts to run and use as test contexts
    shell_scripts_path = os.path.join(configs_path, project_name)
    scripts = sorted(glob.glob(f"{shell_scripts_path}/*.sh"))
    contexts = [os.path.basename(script)[:-3].split("-")[-1] for script in scripts]

    # simulating github checks
    for context in contexts:
        print(context, ": pending")

    dependency_scripts = ["setup", "dependency_install"]
    print("All contexts:", contexts)

    string_output = ""
    for index, script in enumerate(scripts):
        current_context = contexts[index]

        args = [
            "/bin/bash", 
            script,
            author,
            "master",
            project_base_directory
        ]
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        string_output += process.stdout.decode("utf-8")
        if process.returncode != 0:
            # send a github error check
            print("errored at:", current_context)
            if current_context in dependency_scripts:
                # send failed for all the other ones
                for context in contexts[index+1:]:
                    print("did not run:", context)
                    # github_checks.create_status(status=github_checks.ERROR, context=context, description="Your tests failed on GradiaCI!")
                break
            continue 

        # get the last line of the ouput and if it echo's success then send a github pass else send failed
        status = get_last_line(output=process.stdout)
        if status == "status: success":
            print(f"{current_context}: success")
            # github_checks.create_status(status=github_checks.SUCCESS, context=current_context, description="Your tests passed on GradiaCI!")
        else:
            print(f"{current_context}: failed")
            # github_checks.create_status(status=github_checks.ERROR, context=current_context, description="Your tests failed on GradiaCI!")

    with open("test-output.txt", "w") as output_file:
        output_file.write(string_output)


        # while True:
        #     output = process.stdout.readline().decode().strip()
        #     if output == "" and process.poll() is not None:
        #         break 
        #     if output:
        #         # check for the line and find the context
        #         context_found = re.match(r"^context: ", output)
        #         if context_found:
        #             print("Found:", output.lstrip("context:"))
        #         print(output.strip())


    

    # output_stream = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # with open("test-output.txt", "w") as output_file:
    #     output_file.write(output_stream.stdout.decode("utf-8"))


output = run_shell_script()
print("Shell script finished and saved")
