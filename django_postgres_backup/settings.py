from django.conf import settings

DATABASES = getattr(settings, "DATABASES")
if DATABASES is None:
    raise ValueError("'DATABASES' must be defined in settings.")

DATABASE_DEFAULT = getattr(DATABASES, "default")
if DATABASE_DEFAULT is None:
    raise ValueError("'default' must be defined in 'DATABASES'")

DATABASE_NAME = getattr(DATABASE_DEFAULT, "NAME")
if DATABASE_DEFAULT is None:
    raise ValueError("'NAME' must be defined in 'default'")

DATABASE_USER = DATABASE_DEFAULT["USER"]
if DATABASE_USER is None:
    raise ValueError("'USER' must be defined in 'default'")

DEFAULT_POSTGRES_BACKUP_GENERATIONS = 3
POSTGRES_BACKUP_GENERATIONS = (
    getattr(settings, "POSTGRES_BACKUP_GENERATIONS")
    if getattr(settings, "POSTGRES_BACKUP_GENERATIONS")
    else DEFAULT_POSTGRES_BACKUP_GENERATIONS
)
if POSTGRES_BACKUP_GENERATIONS < 1:
    raise ValueError("'POSTGRES_BACKUP_GENERATIONS' must be defined at lest 1.")
