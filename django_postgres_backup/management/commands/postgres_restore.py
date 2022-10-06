from django.core.management import BaseCommand

from django_postgres_backup.common import (
    DEFAULT_BACKUP_DIR,
    DEFAULT_DATABASE_BACKUP_FORMAT,
    backup_path,
    restore_database,
)
from django_postgres_backup.settings import DATABASE_NAME, DATABASE_USER


class Command(BaseCommand):
    help = "Restore a backup for Postgresql."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dbname",
            "-d",
            metavar="DBNAME",
            default=DATABASE_NAME,
            help="database name to backup",
        )
        parser.add_argument(
            "--name", "-f", metavar="NAME", help="name of the backup to restore from which to restore the databse"
        )
        parser.add_argument(
            "--format", "-fo", metavar="FORMAT", default=DEFAULT_DATABASE_BACKUP_FORMAT, help="backup format type"
        )
        parser.add_argument("--username", "-u", metavar="USERNAME", default=DATABASE_USER, help="database username")
        parser.add_argument(
            "--clean",
            "-c",
            action="store_true",
            help="delete database objects before recovery",
        )
        parser.add_argument(
            "--if-exists",
            action="store_true",
            help="use IF EXISTS when objects are deleted",
        )
        parser.add_argument(
            "--backup-dir",
            "-b",
            metavar="BACKUP_DIR",
            default=DEFAULT_BACKUP_DIR,
            help="directory where the backups are stored",
        )

    def handle(self, *args, **options):
        database_name = options["dbname"]
        name = options["name"]
        database_format = options["format"]
        username = options["username"]
        clean = options["clean"]
        if_exists = options["if_exists"]
        backup_dir = options["backup_dir"]

        restore_database(
            clean, if_exists, database_name, database_format, username, backup_path(backup_dir, database_name, name)
        )
