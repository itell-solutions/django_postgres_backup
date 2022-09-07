from django.core.management import BaseCommand

from django_postgres_backup.common import BACKUP_PATH, DEFAULT_DATABASE_BACKUP_FORMAT, backup_and_cleanup_database, run
from django_postgres_backup.settings import DATABASE_NAME, DATABASE_USER, POSTGRES_BACKUP_GENERATIONS


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
        parser.add_argument("--file", "-f", metavar="FILENAME", default=DATABASE_NAME)
        parser.add_argument("--format", "-fo", metavar="FORMAT", default=DEFAULT_DATABASE_BACKUP_FORMAT)
        parser.add_argument("--username", "-u", metavar="USERNAME", default=DATABASE_USER)
        parser.add_argument("--generation", "-g", metavar="GENERATION", default=POSTGRES_BACKUP_GENERATIONS, type=int)
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
        generation = options["generation"]
        path = options["path"]

        print("Making backup directory if necessary.")
        run(["mkdir", "-p", "backup"])

        backup_and_cleanup_database(database_format, database_name, file_name, generation, username, path)
