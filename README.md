### GRADIA Testing Platform (Written to support only Github)
A platform that listens for push event on github repos and performs operations including;  
- pulling the new changes made
- running tests 
- pushing to deployment (future feature)


### How does it work?
This platform uses github **webhooks** in conjunction with github's **deploy keys access to repos** to
make listening for pushes and pulling from repos respectively work.
The process is as follows. The platform:
1. Listens for push events (Github webhook notifications makes this possible). [Webhook's docs](https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks)
2. When a push notification is received, 
    - A script is run for the repo receiving the push. In the script,
        - a pull is made to get the latest changes on the specific branch receiving the push. [Github deploy keys](https://gist.github.com/zhujunsan/a0becf82ade50ed06115) is the preferred way to do this so we would not need to enter our password during the pull.
        - environments are enabled / created if necessary
        - dependencies are installed
        - tests are run
    - A response is sent back to github, indicating the notification was received.
3. After the push notification is received and processed (i.e. tests are run), emails are sent to 
Hello world
**involving parties**.


### Contributing Guidelines
This platform is built using github's webhook's functionality. A webhook is basically is a method of modifying the behaviour of a web app using custom callbacks. (They can also be thought of as automated messages sent from a web app when some event occurs) This is the mechanism we use to receive the notifications from github. When a push is made to a repo, github sends a `request` with some `request data` (`{}`) to a webserver configured on the repo's webhook's settings tab on github. Usually, the webserver is configured to have a route `/payload/` which is configured on github to receive the notification `requests`. The request data contains information we need to understand the **push event** including;
- repo name
- branch
- commit hashes (previous and new)
- author
- etc
We built this platform mainly around github's webhook functionality.


##### Implementation Details
Python / Flask is the main tech stack used in building the platform. It is very minimal. 
It has the following url routes.   
`/`             -  Just for testing to be sure the server is up and running.    
`/payload/`     -  The endpoint where we receive the github push notifications.    

This web server is a multi-threading web server. This means, whenever it accepts a request, it passes it to an execution thread which runs the script and send the summary to the **involving parties**.

It uses a **functional programming** (seen mainly in the `scripts.py` file) approach as its main design paradigm.  
The email sending functionality is built around `sendgrid`  
  
Every repo configured to use this platform has a `shell script` (name of script has a format `repo-name-config.sh`) in some location configured in an environment file `.env` in the root of the project.
In the `ExecutionThread`, the `shell script` is run with python and the output is redirected in python and logged (saved) into 
a file. This output (of the test run) file is sent by email to the **involving parties**.

There are other `functions` implemented to be used in **future features** to extract passed tests, failed tests and errored tests from the output of the test run. These extracts are going to be used to construct an organized summary and sent via email in addition to the whole test file.


##### Installation
After cloning the repo, `cd` into the project repo: `cd CI-SERVER` by default.
1. activate your virtualenv and install the python dependencies: `pip install -r requirements39.txt`
2. setup your environment variables in the root the application. (i.e. You create a `.env` file in the root of the application and set the following variables.)
    - `CONFIGS_PATH` -- location (directory) of the shell scripts.
    - `LOG_OUTPUT_PATH` -- location (directory) where the test outputs are going to generated.
    - `PROJECT_PATH` -- location (directory) where project needs to be clone to.
3. python `app.py`


##### Configuring a github project (repo) to use this platform.
1. Setup webhook url to that repo.
    Github accepts only `https` schemes. So for devs:
    - We use [ngrok](https://ngrok.com/) to open our `server:port` to the internet and get an `https` scheme url.
        - This url is temporal and changes everytime you restart the ngrok server and that is because it's the free version.
        - This is not specific to GRADIA projects on python anywhere.
        - With GRADIA projects configurations, the Payload URL is (https://gradiastaging.pythonanywhere.com/payload/)
    - Content type (application/json)
2. Setup deploy keys for that repo. Get deploy keys from deployment server(pythonanywhere.com) and set for that repo.
    - Here, generate a new ssh key (that is going to be our deploy key) on the server with the name (`id_rsa_repo_name`) and no passphrase. `ssh-keygen -t rsa -C “Deploy key for Repo Name”`
    - Add this newly generated ssh key to the git config file (`~/.ssh/config`) as follows (assuming `/home/user/.ssh/{github-profile-name}/id_rsa_repo_name` is the full path to the newly generated ssh key and `user` is the name of the server username):
        ```
        Host id_rsa_repo_name_alias github.com
        Hostname github.com
        IdentityFile /home/user/.ssh/{github-profile-name}/id_rsa_repo_name
        # User user
        ```
    - Copy the newly generated deploy keys and add to the repo's settings on github: `https://github.com/{user}/{repo}.git` at the **Deploy Keys** tab.

3. Add the shell script for running the tests
    - write the shell script and save as `project_name-config.sh`
    - save the shell script in the `CONFIGS_PATH`
    - Test the shell script with the python script: `python run_script project_name`
3. Voila!! All done.



### Future (Intended) features
Find a way to show a check pass on github if tests are passing.
Prob, use a link that point to an endpoint of the server. If there
is no failing tests, it will return a green svg icon as a response 
indicating a pass and returns a red svg icon otherwise.


### Research Resources:
- [Webhook's docs](https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks)
- [Deploy keys](https://gist.github.com/zhujunsan/a0becf82ade50ed06115)
- [using mltiple Deploy Keys on the same server](https://snipe.net/2013/04/11/multiple-github-deploy-keys-single-server/)
