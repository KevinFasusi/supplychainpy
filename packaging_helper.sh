#!/bin/bash
# This script takes three arguments, the name of the package, the conda environment name and the packaging type (e.g. sdist, bdist_wheel). The script
# activates the environment cleans the previous packaged distribution from the dist folder, creates a new build

installed_package=$1
environment_name=$2
package_type=$3

echo "activating conda environment named: $environment_name"

source activate $environment_name

function clean_env {
    pip uninstall $installed_package
}

function package_dist {
    rm -r dist/ 
    python setup.py $package_type
}

function install_package {
    cd dist
    package=$(ls)
    pip install ${package[0]}
    echo
    echo "NEW INSTALL COMPLETED: Package ${package[0]} installed successfully."
    cd ..
}

clean_env installed_package

package_dist

install_package