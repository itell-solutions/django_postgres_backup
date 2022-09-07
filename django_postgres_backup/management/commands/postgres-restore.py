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
)

YYYY_MM_DD_HH_MM = f"{timezone.now().strftime('%Y-%m-%d-%H-%M')}"
DEFAULT_FORMAT = "t"

BACKUP_PATH = BASE_DIR / "backup"
SUBPROCESS_ENVIRONMENT = os.environ.copy()


def _args_from_command(command: str):
    return command.split(" ")


def _run(command, shell=False):
    if isinstance(command, str):
        print(command)
    else:
        print(" ".join(command))
    subprocess.check_call(command, cwd=BASE_DIR, shell=shell, env=SUBPROCESS_ENVIRONMENT)


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
        parser.add_argument("--format", "-fo", metavar="FORMAT", default=DEFAULT_FORMAT)
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

        restore_database(clean, if_exists, database_name, database_format, username, backup_file(file_name, path))


def backup_file(file_name: str, path: str):
    if file_name:
        file = file_name
    else:
        backup_glob_pattern = os.path.join(
            path, f"{DATABASE_NAME}-20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]_[0-2][0-9]-[0-6][0-9].sql.bz2"
        )
        file = sorted(glob.glob(backup_glob_pattern), reverse=True)[0]
    print(f"Selecting recent backup {file}")

    return file


def restore_database(clean: bool, if_exists: bool, database_name: str, database_format: str, username: str, file: str):
    additional_commands = ""
    if clean:
        additional_commands = "--clean"
    if if_exists:
        additional_commands = f"{additional_commands} --if-exists"

    command = (
        f"PGPASSWORD={DATABASE_PASSWORD} pg_restore --host={DATABASE_HOST} --port={DATABASE_PORT} "
        f"--username={username} --dbname={database_name} --format={database_format} {additional_commands}"
    )

    if file.rsplit(".", 1)[-1] == "bz2":
        command = f"sudo -S bzip2 -d -c {file} -k | {command}"
    else:
        command = f"sudo -S {command} {file}"

    _run([command], True)
