from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoPostgresBackup(AppConfig):
    """
    Config for django_postgres_backup application.
    """

    name = "django_postgres_backup"
    verbose_name = _("Django Postgres Backup")
    default_auto_field = "django.db.models.AutoField"
