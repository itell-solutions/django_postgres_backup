# Contributing

This document describes how to work with the project as developer or potential
contributor.

## Project setup

To get started with the project perform the following steps:

1. Check out the source code:
   ```bash
   git clone https://github.com/itell-solutions/django_postgres_backup
   ```
2. Install [pre-commit](https://pre-commit.com/).
3. Activate pre-commit:
   ```bash
   pre-commit install --install-hooks
   ```
4. Install [poetry](https://python-poetry.org/).
5. Build the project (to put everything in place):
   ```bash
   poetry build
   ```
6. Run the test suite:
   ```bash
   poetry run pytest
   ```

You can edit the source code with any text editor. Additionally, the project
already contains everything needed to open it in PyCharm.

To check the test coverage, run

```bash
poetry run pytest --cov django_postgres_backup --cov-report html
```

and then open `htmlcov/index.html` in your web browser.

## Publish a new release

The following steps are only possible if you have a proper PyPI token set up.

1. Check that every issue of the release
   [milestone](https://github.com/itell-solutions/django_postgres_backup/milestones)
   has been closed.
2. Checkout out the current main:
   ```bash
   git checkout main
   git pull
   ```
3. Check that everything has been committed by ensuring no changes show with:
   ```bash
   git status
   ```
4. Run the test suite:
   ```bash
   poetry run pytest
   ```
5. Publish the release:
   ```bash
   poetry publish
   ```
6. Add a tag matching the version of the release:
   ```bash
   git tag -a -m "Tagged v1.x.x." v1.x.x
   git push origin --tags
   ```
7. Close the related release
   [milestone](https://github.com/itell-solutions/django_postgres_backup/milestones).
