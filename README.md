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

To add validation to your project, add it to `settings.INSTALLED_APPS`.

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
python manage.py postgres_backup --clean --if-exists
```

## Configuration

You can set up how many generations of backup should be saved, all other will be deleted.

```python
POSTGRES_BACKUP_GENERATIONS = 3
```

## Limitations

- Backup and restore works only with postgresql.

## License

Copyright (c) 2022 ITELL.SOLUTIONS GmbH, Graz, Austria.

Distributed under the
[MIT license](https://en.wikipedia.org/wiki/MIT_License). For details refer to
the file `LICENSE`.

The source code is available from
<https://github.com/itell-solutions/django_html_xml_validator>.
