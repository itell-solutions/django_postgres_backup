import os

from django.core.management import BaseCommand

from django_postgres_backup.common import (
    DEFAULT_BACKUP_DIR,
    DEFAULT_DATABASE_BACKUP_FORMAT,
    backup_and_cleanup_database,
)
from django_postgres_backup.settings import DATABASE_NAME, DATABASE_USER, POSTGRES_BACKUP_GENERATIONS


class Command(BaseCommand):
    help = "Backup PostgreSQL database with multiple generations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--backup-dir",
            "-b",
            default=DEFAULT_BACKUP_DIR,
            metavar="BACKUP_DIR",
            help="directory where the backups are stored, default: %(default)s",
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
            "--generations",
            "-g",
            default=POSTGRES_BACKUP_GENERATIONS,
            metavar="GENERATIONS",
            type=int,
            help="maximum number of backups to be kept saved, default: %(default)d",
        )
        parser.add_argument(
            "--name", "-n", default=DATABASE_NAME, metavar="NAME", help="name of the to be created backup"
        )
        parser.add_argument("--username", "-u", default=DATABASE_USER, metavar="USERNAME", help="database username")

    def handle(self, *args, **options):
        database_name = options["dbname"]
        name = options["name"]
        database_format = options["format"]
        username = options["username"]
        generation = options["generations"]
        backup_dir = options["backup_dir"]

        print("Making backup directory if necessary.")
        os.makedirs(backup_dir, exist_ok=True)

        backup_and_cleanup_database(database_format, database_name, name, generation, username, backup_dir)
