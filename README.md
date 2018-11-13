# Production tools for Data Science

This is a bare-bones repository demonstrating how to set up tools for data science projects that will help you write higher quality code. Much of this is inspired by my own experiences at work, and by the project template for scikit-learn projects that is hosted [here](https://github.com/scikit-learn-contrib/project-template).

The repository contains a very simple pipeline, that trains a random forest on the MNIST data set. The code is built as an Airflow directed acyclic graph (DAG), pytest is used for the unit tests, Sphinx to build the documentation, and Circle CI for continuous integration.

## Virtualenv and requirements.txt

When setting up a new project, list out the Python dependencies in a `requirements.txt` file, including the version numbers. Commit this file to the repository, so that every new user can replicate the environment your codebase needs to run in.

Users can create a new environment by using `virtualenv`:

```bash
# This creates the virtual environment
cd $PROJECT_PATH
virtualenv production-tools
```

and then install the dependencies by referring to the `requirements.txt`:

```bash
# This installs the modules
pip install -r requirements.txt

# This activates the virtual environment
source production-tools/bin/activate
```

## Sphinx 

[Sphinx](http://www.sphinx-doc.org/en/stable/) is a plug-in that can be used to build the documentation of your codebase, using the docstrings you put in your code. Sphinx provides an utility called `sphinx-quickstart`, that can be run to get a number of template files that will work out of the box. 

The files in the `docs` folder are the output of running `sphinx-quickstart`. It generates four files:

- `conf.py`: A Python file that contains the configuration for the Sphinx project.
- `index.rst`: A text file that functions as the home page of your documentation.
- `Makefile`: A Makefile that can be used to generate the documentation.
- `make.bat`: A BAT script that can be executed to generate the documentation on Windows.

However, I have made some minor changes:

- At the top of `conf.py`, I import the `sphinx_rtd_theme` module for a custom HTML theme. This also requires a change on lines 87 and 116.
- I add a number of extensions by default on line 43.
- I have created a text file `dags.rst` that contains the documentation of our codebase.

Every user that has access to the codebase, can now build the documentation locally using the provided Makefile. Alternatively, you can build the documentation as part of your build process (using Circle CI), and then host the HTML pages on an (internal) webserver. There is also a [Sphinx confluence plug-in](https://pypi.org/project/sphinx-confluence/), if your company prefers to host documentation on Confluence.

## Circle CI

[Circle CI](https://circleci.com/) is used for continuous integration, but you could use any kind of continuous integration tool here (like Travis, or Jenkins). All you need to use Circle CI in your repository is a `config.yml` file in the `.circleci` directory, and an account on [circleci.com](https://circleci.com/). You can connect that account with your GitHub account, and Circle CI will then scan your repositories and tell you for which ones it can enable automatic builds. 

In this repository, we only use Circle CI to run the unit tests every time a pull request is opened. However, you can customize this so that you can execute more tasks when a PR is submitted. For example, you could add:

- Building the documentation to ensure it is not broken with the proposed changes.
- Installing the repository if it is meant to be shipped as a Python package. 
- Execute data pipelines that are part of the DAGs in the codebase (integration tests).

Check out the [Circle CI website](https://circleci.com/docs/2.0/tutorials/) for an in-depth tutorial on how to configure Circle CI workflows.

## Black as a pre-commit linter

[Black](https://github.com/ambv/black) is used as a pre-commit linter. You should follow the instructions in their repo on how to set it up. In essence you need to:

- Install `black` using `pip`.
- Install `pre-commit` using `pip`.
- Copy the `.pre-commit-config.yaml` file into your repository.
- Run `pre-commit install`.

## Airflow

[Airflow](https://airflow.apache.org/) is used to build the workflow as a DAG, and it can be found in the `pipeline.dags` module. 
