from django.conf import settings

BASE_DIR = getattr(settings, "BASE_DIR", None)
if BASE_DIR is None:
    raise ValueError("'BASE_DIR' must be set as the base directory of the project.")

DATABASES = getattr(settings, "DATABASES", None)
if DATABASES is None:
    raise ValueError("'DATABASES' must be defined in settings.")

DATABASE_DEFAULT = DATABASES.get("default")
if DATABASE_DEFAULT is None:
    raise ValueError("'default' must be defined in 'DATABASES'")

DATABASE_NAME = DATABASE_DEFAULT.get("NAME")
if DATABASE_NAME is None:
    raise ValueError("'NAME' must be defined in 'default'")

DATABASE_USER = DATABASE_DEFAULT.get("USER")
if DATABASE_USER is None:
    raise ValueError("'USER' must be defined in 'default'")

DATABASE_HOST = DATABASE_DEFAULT.get("HOST")
if DATABASE_HOST is None:
    raise ValueError("'HOST' must be defined in 'default'")

DATABASE_PORT = DATABASE_DEFAULT.get("PORT")
if DATABASE_PORT is None:
    raise ValueError("'PORT' must be defined in 'default'")

DATABASE_PASSWORD = DATABASE_DEFAULT.get("PASSWORD")
if DATABASE_PASSWORD is None:
    raise ValueError("'PASSWORD' must be defined in 'default'")

DEFAULT_POSTGRES_BACKUP_GENERATIONS = 3
DEFAULT_POSTGRES_BACKUP_DIR = BASE_DIR / "backup"
POSTGRES_BACKUP_GENERATIONS = (
    getattr(settings, "POSTGRES_BACKUP_GENERATIONS", None)
    if getattr(settings, "POSTGRES_BACKUP_GENERATIONS", None)
    else DEFAULT_POSTGRES_BACKUP_GENERATIONS
)
if POSTGRES_BACKUP_GENERATIONS < 1:
    raise ValueError("'POSTGRES_BACKUP_GENERATIONS' must be defined at lest 1.")
POSTGRES_BACKUP_DIR = (
    getattr(settings, "POSTGRES_BACKUP_DIR", None)
    if getattr(settings, "POSTGRES_BACKUP_DIR", None)
    else DEFAULT_POSTGRES_BACKUP_DIR
)
