import bz2
import glob
import os
import subprocess
from tempfile import NamedTemporaryFile
from typing import Optional

from django.utils import timezone

from django_postgres_backup.settings import BASE_DIR, DATABASE_HOST, DATABASE_PASSWORD, DATABASE_PORT

DEFAULT_BACKUP_DIR = BASE_DIR / "backup"
DEFAULT_DATABASE_BACKUP_FORMAT = "t"
YYYY_MM_DD_HH_MM = f"{timezone.now().strftime('%Y-%m-%d_%H-%M')}"

ADMIN_USERNAME = "admin"


def backup_and_cleanup_database(
    database_format: str,
    database_name: str,
    name: str,
    generation: int,
    username: str,
    path: str,
):
    file_name_with_timestamp = f"{name}-{YYYY_MM_DD_HH_MM}"
    command = [
        "pg_dump",
        "--host",
        DATABASE_HOST,
        "--port",
        str(DATABASE_PORT),
        "--username",
        username,
        "--dbname",
        database_name,
        "--format",
        database_format,
        "--no-password",
    ]

    with NamedTemporaryFile() as database_dump_file:
        run(command, database_dump_file)
        database_dump_file.seek(0)
        with bz2.open(os.path.join(DEFAULT_BACKUP_DIR, f"{file_name_with_timestamp}.sql.bz2"), "wb") as compressed_file:
            compressed_file.write(database_dump_file.read())

    delete_older_backup_files(
        name,
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


def backup_path(
    backup_path: str,
    database_name: str,
    file_name: Optional[str] = None,
) -> str:
    if file_name:
        file = file_name
    else:
        backup_glob_pattern = os.path.join(
            backup_path, f"{database_name}-20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]_[0-2][0-9]-[0-6][0-9].sql.bz2"
        )
        file = sorted(glob.glob(backup_glob_pattern), reverse=True)[0]
    print(f"Selecting recent backup {file}")

    return file


def restore_database(
    clean: bool,
    if_exists: bool,
    database_name: str,
    database_format: str,
    username: str,
    name: str,
):
    command = [
        "pg_restore",
        "--host",
        DATABASE_HOST,
        "--port",
        str(DATABASE_PORT),
        "--username",
        username,
        "--dbname",
        database_name,
        "--format",
        database_format,
    ]

    if clean:
        command.append("--clean")
    if if_exists:
        command.append("--if-exists")
    if name.rsplit(".", 1)[-1] == "bz2":
        with NamedTemporaryFile() as tmp_file:
            with bz2.open(name, "rb") as compressed_file:
                tmp_file.write(compressed_file.read())
            tmp_file.seek(0)
            run(command, input_file=tmp_file.read())
    else:
        with open(name, "rb") as backup_file:
            run(command, input_file=backup_file.read())


def run(command, output_file: Optional[NamedTemporaryFile] = None, input_file: Optional[NamedTemporaryFile] = None):
    if isinstance(command, str):
        print(command)
    else:
        print(" ".join(command))
    capture_output = output_file is None
    env = os.environ.copy()
    env["PGPASSWORD"] = DATABASE_PASSWORD
    subprocess.run(command, stdout=output_file, input=input_file, capture_output=capture_output, check=True, env=env)
