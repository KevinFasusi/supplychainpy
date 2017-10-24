#!/bin/bash
# Author Kevin Fasusi
# MIT licence
# This script takes two arguments, the name of the package and the conda environment name. The script
# activates the environment cleans the previous packaged distribution from the dist folder, creates a new build
# and finally installs the new package.
# LICENSE, README.md, .gitignore, setup.py, requirements.txt, Dockerfile
# A License is requested and populated, using the website licenses.opendefinition.org

installed_package=$1
environment_name=$2

if [[ $MACHTYPE == "x86_64-apple-darwin16" ]]; then
    package_manager="gpip" 
else
    package_manager="pip"
fi


echo "activating conda environment named: $environment_name"

source activate $environment_name

function clean_env {
    gpip uninstall $1
}

function package_dist {
    rm -r dist/ 
    python setup.py sdist
}

function install_package {
    cd dist
    package=$(ls)
    $package_manager install ${package[0]}
    echo "NEW INSTALL COMPLETED: Package ${package[0]} installed successfully."
    cd ..
}

clean_env installed_package

package_dist

install_package