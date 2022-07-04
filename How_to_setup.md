# How to setup

This document describes the process how to setup and use the pre-commit-dbt in your dbt projects

## 1. Install package pre-commit
Before you can run hooks, you need to have the pre-commit package manager installed.

``` bash
    pip install pre-commit
```

Check if it was installed successfully:

``` bash
    $ pre-commit --version
    pre-commit 2.19.0
```

## 2. Add a pre-commit configuration

- create a file named `.pre-commit-config.yaml`
- you can generate a very basic configuration using `@pre-commit sample-config`
  - make sure to use the right repo : `https://github.com/artefactory/pre-commit-dbt` in the `.pre-commit-config.yaml`
- List the hooks you want to use in the `.pre-commit-config.yaml` file

Example:
```
repos:
-   repo: https://github.com/artefactory/pre-commit-dbt
    rev: v1.0.0
    hooks:
    -  id: check_exposure_has_owner
    -  id: check-exposure-folder-constraint
    -  id: source-folder-constraint
    -  id: check-model-has-contract
```

## 3. Install the git hook scripts

- run `pre-commit install` to set up the git hook scripts
```bash
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```
- now `pre-commit` will run automatically on `git commit!`

## Usage
- If you want to manually run all `pre-commit` hooks on a repository run :
``` bash
$ pre-commit run --all-files
```
 - To run individual hooks use :
```bash
 $ pre-commit run <hook_id>
```