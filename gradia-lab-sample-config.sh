#!/bin/bash

# To provide a little context on the nature of these shell configuration files:
# This configuration file is specific to GRADIA specifications. i.e python version (3.9), 
#  name requirements file requirements39.txt, etc


# variables
owner=$1
branch_name=$2
project_base_directory_path=$3
project_directory_path="${project_base_directory_path}${owner}/gradia-lab-sample"
underline="==================================================================="

echo "branch name: $branch_name"
echo "project base path: $project_base_directory_path"
echo "project directory path: $project_directory_path"
echo $underline 

# create a virtualenv if it doesn't exist
if [ ! -d "~/.environments/${owner}/gradia-lab-sample/" ]; then 
    echo "Creating python virtual environment..."
    echo $underline
    mkdir -p "~/.environments/${owner}"
    python3 -m venv "~/.environments/${owner}/gradia-lab-sample"
    echo $underline
fi

# active virtual env 
echo "Activating python virtual environment.."
echo $underline
source "~/.environments/${owner}/gradia-lab-sample/bin/activate"
echo $underline 

if [! -d $project_directory_path ]; then 
    # Do cloning here
    echo "Project does not exit"
    echo "Cloning Project..."
    pushd "$project_base_directory_path"
    git clone "$owner-gradia-lab-sample:${owner}/gradia-lab-sample.git"
fi
echo "changing directory to: $project_directory_path"
pushd "$project_directory_path"
git remote -v

echo "Checkout to branch: $branch_name..."
echo $underline
git checkout -f $branch_name
echo $underline 

# Pulling recent changes
echo "Pulling changes..."
echo $underline 
git pull upstream $branch_name  # on pythonanywhere this will be `git pull origin frontend-looser-ratelimit`
echo $underline 

# install requirements for both fresh and updated dependency instances 
echo "Installing python dependencies..."
echo $underline
pip install -r requirements39.txt
echo $underline 

# run frontend dependency install 
echo "Installing frontend (react) dependencies..."
echo $underline
cd frontend && npm install
echo $underline

# running frontend build 
echo "Building frontend (react) files..."
echo $underline
npm run build 
echo $underline


# Testing comes here

# linting frontend
echo "Checking linting..."
echo $underline
npm run lint
echo $underline 

# linting backend 
echo "Checking black formatting"
echo $underline 
cd .. && black --line-length 117 --exclude '^.*\b(migrations)\b.*$' --check django_backend selenium_tests
echo $underline 

# unittests
echo "Running django unittests"
echo $underline 
cd django_backend && pytest 
echo $underline 

# # selenium test
# cd ../selenium_tests && pytest 

