[![PyPI](https://img.shields.io/pypi/v/django_postgres_backup)](https://pypi.org/project/django_postgres_backup/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django_postgres_backup.svg)](https://www.python.org/downloads/)
[![Build Status](https://github.com/itell-solutions/django_postgres_backup/actions/workflows/build.yaml/badge.svg)](https://github.com/itell-solutions/django_postgres_backup/actions/workflows/build.yaml)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/itell-solutions/django_postgres_backup)](https://opensource.org/licenses/MIT)

# Django managed commands to backup and restore PostgreSQL databases with multiple generations

The `django_postgres_backup` Django module includes managed commands to back
up and restore a PostgreSQL database with time stamped names to provide
multiple backup generations.

## Installation

To install, depending on your package manager, run:

```bash
pip install --update django_postgres_backup
```

or

```bash
poetry add django_postgres_backup
```

## Usage

To add the backup related managed commands to your project, add it to
`settings.INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...,
    "django_postgres_backup",
]
```

After this, you can backup the default database by running:

```bash
python manage.py postgres_backup
```

The created backup can now be restored by running:

```bash
python manage.py postgres_backup
```

You can clean and restore a whole database with all the tables and data

```bash
python manage.py postgres_restore --clean --if-exists
```

## Configuration

You can set up how many generations of backup should be saved, all other will be deleted.

```python
POSTGRES_BACKUP_GENERATIONS = 3
```

## Limitations

Backup and restore works only with postgresql.

## License

Copyright (c) 2022 ITELL.SOLUTIONS GmbH, Graz, Austria.

Distributed under the
[MIT license](https://en.wikipedia.org/wiki/MIT_License). For details refer to
the file `LICENSE`.

The source code is available from
<https://github.com/itell-solutions/django_postgres_backup>.
