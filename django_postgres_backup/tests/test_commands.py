import unittest

import psycopg2

from django_postgres_backup.common import (
    BACKUP_PATH,
    DEFAULT_DATABASE_BACKUP_FORMAT,
    backup_and_cleanup_database,
    backup_file,
    restore_database,
)
from django_postgres_backup.settings import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USER,
)

TEST_CAR_NAME = "Audi"
TEST_CREATE_DATABASE_SQL = f"create database test{DATABASE_NAME};"
TEST_CREATE_TABLE_CARS_SQL = "create table cars (id SERIAL PRIMARY KEY , name VARCHAR(255) NOT NULL);"
TEST_SELECT_FROM_CARS_SQL = "select * from cars;"
TEST_DROP_CARS_TABLE_SQL = "drop table cars;"
TEST_DROP_DATABASE_SQL = f"drop database test{DATABASE_NAME};"


class BackupRestoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.con = psycopg2.connect(
            database=f"test_{DATABASE_NAME}",
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            port=DATABASE_PORT,
        )
        self.con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.con.cursor()
        self.cursor.execute(TEST_CREATE_DATABASE_SQL)
        self.cursor.execute(TEST_CREATE_TABLE_CARS_SQL)

    def tearDown(self) -> None:
        self.cursor.execute(TEST_DROP_CARS_TABLE_SQL)
        self.cursor.execute(TEST_DROP_DATABASE_SQL)
        self.con.close()

    def test_can_backup_and_restore_database(self):
        self.cursor.execute(f"insert into cars(name) values('{TEST_CAR_NAME}');")
        self.cursor.execute(TEST_SELECT_FROM_CARS_SQL)
        rows = self.cursor.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == TEST_CAR_NAME

        backup_and_cleanup_database(
            DEFAULT_DATABASE_BACKUP_FORMAT,
            f"test_{DATABASE_NAME}",
            f"test_{DATABASE_NAME}",
            2,
            DATABASE_USER,
            BACKUP_PATH,
            False,
        )

        self.cursor.execute(f"delete from cars where id ={rows[0][0]}")
        self.cursor.execute(TEST_SELECT_FROM_CARS_SQL)
        rows = self.cursor.fetchall()
        assert len(rows) == 0

        restore_database(
            True,
            True,
            f"test_{DATABASE_NAME}",
            DEFAULT_DATABASE_BACKUP_FORMAT,
            DATABASE_USER,
            backup_file(BACKUP_PATH, f"test_{DATABASE_NAME}"),
            False,
        )

        self.cursor.execute(TEST_SELECT_FROM_CARS_SQL)
        rows = self.cursor.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == TEST_CAR_NAME
