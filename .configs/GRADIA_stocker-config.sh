#!/bin/bash

# To provide a little context on the nature of these shell configuration files:
# This configuration file is specific to GRADIA specifications. i.e python version (3.9), 
#  name requirements file requirements39.txt, etc


# create a virtualenv if it doesn't exist
if [ ! -d "~/.environments/GRADIA_stocker_venv/" ]; then 
    mkdir -p ~/.environments
    python3 -m venv ~/.environments/GRADIA_stocker_venv
fi

# active virtual env 
source ~/.environments/GRADIA_stocker/bin/activate

# move into the git repo directory ==> /var/www/sites/GRADIA_stocker
cd ~/development/Gradia\ Limited/GRADIA_stocker/
git pull upstream frontend-looser-ratelimit  # on pythonanywhere this will be `git pull origin frontend-looser-ratelimit`

# install requirements for both fresh and updated dependency instances 
pip install -r requirements39.txt

# run frontend dependency install 
cd frontend && npm run lint

# run frontend build 
npm run build 


# Testing comes here

# linting frontend
# Stocker currency do not have linting tests, TODO: we may want to add that at some point though

# unittests
cd django_backend && pytest 

# selenium test
cd ../selenium_tests && pytest 

