from django.core.management import BaseCommand

from django_postgres_backup.common import BACKUP_PATH, DEFAULT_DATABASE_BACKUP_FORMAT, backup_file, restore_database
from django_postgres_backup.settings import DATABASE_NAME, DATABASE_USER


class Command(BaseCommand):
    help = "Download bootstrap, build template css and copy bootstrap.bundle.min.js"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dbname",
            "-d",
            metavar="DBNAME",
            default=DATABASE_NAME,
            help="database name to backup",
        )
        parser.add_argument("--file", "-f", metavar="FILENAME")
        parser.add_argument("--format", "-fo", metavar="FORMAT", default=DEFAULT_DATABASE_BACKUP_FORMAT)
        parser.add_argument("--username", "-u", metavar="USERNAME", default=DATABASE_USER)
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
            "--path",
            "-p",
            metavar="PATH",
            default=BACKUP_PATH,
        )

    def handle(self, *args, **options):
        database_name = options["dbname"]
        file_name = options["file"]
        database_format = options["format"]
        username = options["username"]
        clean = options["clean"]
        if_exists = options["if_exists"]
        path = options["path"]

        restore_database(
            clean, if_exists, database_name, database_format, username, backup_file(path, database_name, file_name)
        )
