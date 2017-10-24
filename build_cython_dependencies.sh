#!/bin/bash
# Author Kevin Fasusi
# MIT licence
# This script builds the cython dependencies for the project
# LICENSE, README.md, .gitignore, setup.py, requirements.txt, Dockerfile
# A License is requested and populated, using the website licenses.opendefinition.org

environment_name=$1

if [[ $MACHTYPE == "x86_64-apple-darwin16" ]]; then
    #Alias used in on dev machine for pip, to avoid messing with the system environment on the dev machine. 
    package_manager="gpip" 
else
    package_manager="pip"
fi

echo "activating conda environment named: $environment_name"

source activate $environment_name

python setup.py build_ext -i
