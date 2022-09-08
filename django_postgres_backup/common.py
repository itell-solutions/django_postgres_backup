import glob
import os
import subprocess
from typing import Optional

from django.contrib.auth.models import User
from django.utils import timezone

from django_postgres_backup.settings import BASE_DIR, DATABASE_HOST, DATABASE_PASSWORD, DATABASE_PORT
from example_app.models import Cars
from example_project.settings import DEMO_PASSWORD

BACKUP_PATH = BASE_DIR / "backup"
DEFAULT_DATABASE_BACKUP_FORMAT = "t"
YYYY_MM_DD_HH_MM = f"{timezone.now().strftime('%Y-%m-%d_%H-%M')}"

CARS_TO_CREATE = ["Audi", "Mercedes", "BMW"]
ADMIN_USERNAME = "admin"


def backup_and_cleanup_database(
    database_format: str,
    database_name: str,
    file_name: str,
    generation: int,
    username: str,
    path: str,
    is_sudo: bool = True,
):
    file_name_with_timestamp = f"{file_name}-{YYYY_MM_DD_HH_MM}"
    sudo_command = "sudo -S" if is_sudo else ""
    command = (
        f"{sudo_command} PGPASSWORD={DATABASE_PASSWORD} pg_dump --host={DATABASE_HOST} --port={DATABASE_PORT} "
        f"--username={username} --dbname={database_name} --format={database_format} | "
        f"bzip2 -c > backup/{file_name_with_timestamp}.sql.bz2"
    )
    run([command], True)
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


def backup_file(
    path: str,
    database_name: str,
    file_name: Optional[str] = None,
):
    if file_name:
        file = file_name
    else:
        backup_glob_pattern = os.path.join(
            path, f"{database_name}-20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]_[0-2][0-9]-[0-6][0-9].sql.bz2"
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
    file: str,
    is_sudo: bool = True,
):
    additional_commands = ""
    if clean:
        additional_commands = "--clean"
    if if_exists:
        additional_commands = f"{additional_commands} --if-exists"

    command = (
        f"PGPASSWORD={DATABASE_PASSWORD} pg_restore --host={DATABASE_HOST} --port={DATABASE_PORT} "
        f"--username={username} --dbname={database_name} --format={database_format} {additional_commands}"
    )

    sudo_command = "sudo -S" if is_sudo else ""
    if file.rsplit(".", 1)[-1] == "bz2":
        command = f"{sudo_command} bzip2 -d -c {file} -k | {command}"
    else:
        command = f"{sudo_command} {command} {file}"

    run([command], True)


def run(command, shell=False):
    if isinstance(command, str):
        print(command)
    else:
        print(" ".join(command))
    subprocess.check_call(command, cwd=BASE_DIR, shell=shell)


def makedemo():
    if not User.objects.filter(username=ADMIN_USERNAME).exists():
        print("Create super user")
        User.objects.create_superuser(ADMIN_USERNAME, password=DEMO_PASSWORD)
    print(f"Creating demo cars{CARS_TO_CREATE}")
    Cars.objects.bulk_create(Cars(name=name) for name in CARS_TO_CREATE)
