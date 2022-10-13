from django.core.management import BaseCommand

from django_postgres_backup.common import (
    DEFAULT_BACKUP_DIR,
    DEFAULT_DATABASE_BACKUP_FORMAT,
    backup_path,
    restore_database,
)
from django_postgres_backup.settings import DATABASE_NAME, DATABASE_USER


class Command(BaseCommand):
    help = "Restore a backup for PostgreSQL."

    def add_arguments(self, parser):
        parser.add_argument(
            "--backup-dir",
            "-b",
            default=DEFAULT_BACKUP_DIR,
            metavar="BACKUP_DIR",
            help="directory where the backups are stored, default: %(default)s",
        )
        parser.add_argument(
            "--clean",
            "-c",
            action="store_true",
            help="delete database objects before recovery",
        )
        parser.add_argument(
            "--dbname",
            "-d",
            default=DATABASE_NAME,
            metavar="DBNAME",
            help="database name to backup",
        )
        parser.add_argument(
            "--format",
            "-f",
            default=DEFAULT_DATABASE_BACKUP_FORMAT,
            metavar="FORMAT",
            help="accepts postgresql backup format types",
        )
        parser.add_argument(
            "--if-exists",
            "-i",
            action="store_true",
            help="remove possibly existing database objects before restoring them",
        )
        parser.add_argument(
            "--name", "-n", metavar="NAME", help="name of the backup to restore from which to restore the databse"
        )
        parser.add_argument("--username", "-u", default=DATABASE_USER, metavar="USERNAME", help="database username")

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
