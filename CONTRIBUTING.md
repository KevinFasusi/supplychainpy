## Contributing

Thank you for considering contributing to supplychainpy. Let's build a useful tool that makes all our lives easier.


### Where to start?

The three most likely reasons for contributing are:

- Fixing a bug, you have discovered;
- Closing an open issue, posted by the community; and
- Adding a feature, you would like to see in the project.

If you want to report a bug, please use the [issues](https://github.com/KevinFasusi/supplychainpy/issues) tracker. Check if the issue is already submitted. If the issue is not listed, raise a ticket.

### Fix the issue

If the bug is something you feel you can fix, fork the [repo](https://github.com/KevinFasusi/supplychainpy) and clone to your system using:

```
$ git clone https://github.com/<name-of-your-repo>/supplychainpy
```
And create a branch. Use a descriptive name for the branch for example:

```
$ git checkout -b 203-add-olap-etl

```

### Setting up a Development Environment

A development environment can be set up using the Anaconda package management environment provided by Continuum Analytics.

#### Set up Conda Environment

1. Install Anaconda from [Continuum Analytics](https://www.continuum.io/downloads).

2. Create a conda environment substituting `environment-name` with a memorable name:

    ```
    $ conda create -n environment-name python=3.5
    ```

3. Activate the environment:

    **Windows**

    ```
    C:\ activate environment-name
    ```

    **nix**

    ```
    $ source activate environment-name
    ```

4.    Install requirements for development (make sure you are in the root folder of the supplychainpy library check to see if you can see the dev_requirements.txt file in the current folder):

    ```
    $ pip install dev_requiments.txt
    ```

5. Run all the unit test to verify your environment is setup correctly. This may take some time depending on your machine; you might want to get some coffee. If any of the tests fail due to missing package, install the missing package:

    ```
    $ python -m unittest discover tests/
    ```

6. All good? Awesome! Happy Dev'ing (if not check the issues board and raise a new [issue](https://github.com/KevinFasusi/supplychainpy/issues). Make sure to copy and paste the output. In addition to posting an issue, hop on <a href="#Slack"> slack</a>).


### Library Structure

The library is structured for ease of maintenance. There is a separation between public and private modules, making refactoring or reimplementation less likely to break contracts and minimise non-compatible change to the API. This is a constant battle and the aim is to keep improving.

### Public API

The public API consists of the following modules:

- model_inventory.py
- model_decisions.py
- model_demand.py
- simulate.py

### Reporting Package

Most of the public API modules have corresponding packages with the 'model_' prefix removed, containing the supporting classes and modules. Seperating the interface from the main code, allows easier refactoring and changes to the logic without breaking contracts.

### Supporting Documentation

Each issue marked as 'community' will contain information regarding the contribution. Any relevant module and class currently in the library, will be indicated.

Some tests for the public API may already be written. The tests may either be essential or for guidance and will be indicated accordingly. It is expected that any other tests required will be added by the contributor, to maintain a high level of coverage.

### Docstrings with Examples

For all functions please provide docstrings and examples. The [Google](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) style format followed in this library. If you are using an IDE like [PyCharm](https://www.jetbrains.com/pycharm/?fromMenu) then you can set this style as a [default](https://www.jetbrains.com/help/pycharm/2016.3/python-integrated-tools.html).

### Documentation

All public APIs must be accompanied by documentation in addition to the docstrings. The documentation should detail the functionality and an example. The documentation is located in the docs folder.

Sphinx is used to compile the documentation. All of the documentation is written in restructured text. The markup language guide for rst can be found [here](http://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html).

Add documentation with the following steps:

1. Add an '.rst' file to the main docs folder. Give the file an obvious file name that corresponds to the feature you have implemented.

2. Title the file and document the feature.

3. Add the new file's name to the index.rst file.

4. From the command line navigate to the `docs/` folder and run the following command (make sure you are in the environment with all the dev dependencies installed):

    ```
    $ make clean
    $ sphinx-apidocs -o . ../supplychainpy -f
    $ make html
    ```

### Join the Slack Channel

Reach out! We want to build a friendly collaborative environment with plenty of healthy debate about the direction and the code. Send an [email](mailto:kevin@supplybi.com) requesting an invite to our slack channel and we will get back to you ASAP.