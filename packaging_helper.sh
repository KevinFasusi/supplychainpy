#!/bin/bash
# This script takes three arguments, the name of the package, the conda environment name and the packaging type (e.g. sdist, bdist_wheel). The script
# activates the environment cleans the previous packaged distribution from the dist folder, creates a new build

installed_package=$1
environment_name=$2
package_type=$3

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
    python setup.py $3
}

function install_package {
    cd dist
    package=$(ls)
    $package_manager install ${package[0]}
    echo
    echo "NEW INSTALL COMPLETED: Package ${package[0]} installed successfully."
    cd ..
}

clean_env installed_package

package_dist

install_package