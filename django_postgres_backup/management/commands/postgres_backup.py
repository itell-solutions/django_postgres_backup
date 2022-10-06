import os

from django.core.management import BaseCommand

from django_postgres_backup.common import (
    DEFAULT_BACKUP_DIR,
    DEFAULT_DATABASE_BACKUP_FORMAT,
    backup_and_cleanup_database,
)
from django_postgres_backup.settings import DATABASE_NAME, DATABASE_USER, POSTGRES_BACKUP_GENERATIONS


class Command(BaseCommand):
    help = "Generates a backup for Postgresql and handles backup generations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dbname",
            "-d",
            metavar="DBNAME",
            default=DATABASE_NAME,
            help="database name to backup",
        )
        parser.add_argument(
            "--name", "-n", metavar="NAME", default=DATABASE_NAME, help="name of the to be created backup"
        )
        parser.add_argument(
            "--format", "-fo", metavar="FORMAT", default=DEFAULT_DATABASE_BACKUP_FORMAT, help="backup format type"
        )
        parser.add_argument("--username", "-u", metavar="USERNAME", default=DATABASE_USER, help="database username")
        parser.add_argument(
            "--generations",
            "-g",
            metavar="GENERATIONS",
            default=POSTGRES_BACKUP_GENERATIONS,
            type=int,
            help="maximum number of backups to be kept saved",
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
        generation = options["generations"]
        backup_dir = options["backup_dir"]

        print("Making backup directory if necessary.")
        os.makedirs(backup_dir, exist_ok=True)

        backup_and_cleanup_database(database_format, database_name, name, generation, username, backup_dir)
