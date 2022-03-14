#!/bin/bash

# To provide a little context on the nature of these shell configuration files:
# This configuration file is specific to GRADIA specifications. i.e python version (3.9), 
#  name requirements file requirements39.txt, etc


# create a virtualenv if it doesn't exist
if [ ! -d "~/.environments/gradia-lab-sample/" ]; then 
    mkdir -p ~/.environments
    python3 -m venv ~/.environments/gradia-lab-sample
fi

# active virtual env 
source ~/.environments/gradia-lab-sample/bin/activate

# cd /var/www/sites/gradia-lab-websites
cd ~/development/Gradia\ Limited/gradia-lab-sample/
git pull upstream frontend-looser-ratelimit  # on pythonanywhere this will be `git pull origin frontend-looser-ratelimit`

# install requirements for both fresh and updated dependency instances 
pip install -r requirements39.txt

# run frontend dependency install 
cd frontend && npm run lint

# run frontend build 
npm run build 


# Testing comes here

# linting frontend
npm run lint

# linting backend 
cd .. && black --line-length 117 --exclude '^.*\b(migrations)\b.*$' --check django_backend selenium_tests

# unittests
cd django_backend && pytest 

# selenium test
cd ../selenium_tests && pytest 

