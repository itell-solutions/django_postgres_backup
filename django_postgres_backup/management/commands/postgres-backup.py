# Create restore functionality.
import glob
import os
import subprocess

from django.core.management import BaseCommand
from django.utils import timezone

from django_postgres_backup.settings import (
    BASE_DIR,
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USER,
    POSTGRES_BACKUP_GENERATIONS,
)

YYYY_MM_DD_HH_MM = f"{timezone.now().strftime('%Y-%m-%d_%H-%M')}"
DEFAULT_FORMAT = "t"

BACKUP_PATH = BASE_DIR / "backup"


def _args_from_command(command: str):
    return command.split(" ")


def _run(command, shell=False):
    if isinstance(command, str):
        print(command)
    else:
        print(" ".join(command))
    subprocess.check_call(command, cwd=BASE_DIR, shell=shell)


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
        parser.add_argument("--format", "-fo", metavar="FORMAT", default=DEFAULT_FORMAT)
        parser.add_argument("--username", "-u", metavar="USERNAME", default=DATABASE_USER)
        parser.add_argument("--generation", "-g", metavar="GENERATION", default=POSTGRES_BACKUP_GENERATIONS, type=int)
        parser.add_argument(
            "--docker_container",
            "-c",
            metavar="DOCKER_CONTAINER",
            help="docker container name used for database",
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
        generation = options["generation"]
        path = options["path"]

        print("Making backup directory if necessary.")
        _run(["mkdir", "-p", "backup"])

        backup_and_cleanup_database(database_format, database_name, file_name, generation, username, path)


def backup_and_cleanup_database(
    database_format: str, database_name: str, file_name: str, generation: int, username: str, path: str
):
    file_name_with_timestamp = f"{file_name}-{YYYY_MM_DD_HH_MM}"
    command = (
        f"sudo -S PGPASSWORD={DATABASE_PASSWORD} pg_dump --host={DATABASE_HOST} --port={DATABASE_PORT} "
        f"--username={username} --dbname={database_name} --format={database_format} | "
        f"bzip2 -c > backup/{file_name_with_timestamp}.sql.bz2"
    )
    _run([command], True)
    delete_older_backup_files(
        file_name,
        generation,
        path,
    )


def delete_older_backup_files(
    file_name: str,
    generation: int,
    path: str,
):
    print(f"Cleaning up older backups up until the {generation}")
    backup_glob_pattern = os.path.join(
        path, f"{file_name}-20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]_[0-2][0-9]-[0-6][0-9].sql.bz2"
    )
    backup_files_to_delete = sorted(glob.glob(backup_glob_pattern), reverse=True)[generation:]
    for backup_file_to_delete in backup_files_to_delete:
        print(f"Removing old backup {backup_file_to_delete}")
        os.remove(backup_file_to_delete)
