import unittest

import psycopg2

from django_postgres_backup.common import (
    DEFAULT_BACKUP_DIR,
    DEFAULT_DATABASE_BACKUP_FORMAT,
    backup_and_cleanup_database,
    backup_path,
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
TEST_CREATE_DATABASE_SQL = f"create database {DATABASE_NAME};"
TEST_CREATE_TABLE_CARS_SQL = "create table cars (id serial primary key , name varchar(255) not null);"
TEST_SELECT_FROM_CARS_SQL = "select * from cars;"
TEST_DROP_CARS_TABLE_IF_EXISTS_SQL = "drop table if exists cars;"
TEST_DROP_DATABASE_IF_EXISTS_SQL = f"drop database if exists {DATABASE_NAME};"


class BackupRestoreTest(unittest.TestCase):
    def setUp(self):
        self.connection = None
        self.cursor = None

    def tearDown(self):
        self.connection = None
        self.cursor = None

    def _connect_without_database_name(self):
        self.connection = psycopg2.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            port=DATABASE_PORT,
        )
        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    def _setup_database(self):
        self._connect_without_database_name()
        self.cursor.execute(TEST_DROP_DATABASE_IF_EXISTS_SQL)
        self.cursor.execute(TEST_CREATE_DATABASE_SQL)
        self.cursor.close()
        self.connection.close()

        # Connect again but with newly created database.
        self.connection = psycopg2.connect(
            dbname=DATABASE_NAME,
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            port=DATABASE_PORT,
        )
        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()
        self.cursor.execute(TEST_DROP_CARS_TABLE_IF_EXISTS_SQL)
        self.cursor.execute(TEST_CREATE_TABLE_CARS_SQL)

    def _test_can_backup_and_restore_database(self):
        self.cursor.execute(f"insert into cars(name) values('{TEST_CAR_NAME}');")
        self.cursor.execute(TEST_SELECT_FROM_CARS_SQL)
        rows = self.cursor.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == TEST_CAR_NAME

        backup_and_cleanup_database(
            DEFAULT_DATABASE_BACKUP_FORMAT,
            f"{DATABASE_NAME}",
            f"{DATABASE_NAME}",
            2,
            DATABASE_USER,
            DEFAULT_BACKUP_DIR,
        )

        self.cursor.execute(f"delete from cars where id ={rows[0][0]}")
        self.cursor.execute(TEST_SELECT_FROM_CARS_SQL)
        rows = self.cursor.fetchall()
        assert len(rows) == 0

        restore_database(
            True,
            True,
            DATABASE_NAME,
            DEFAULT_DATABASE_BACKUP_FORMAT,
            DATABASE_USER,
            backup_path(DEFAULT_BACKUP_DIR, DATABASE_NAME),
        )

        self.cursor.execute(TEST_SELECT_FROM_CARS_SQL)
        rows = self.cursor.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == TEST_CAR_NAME

    def test_can_backup_and_restore_database(self):
        try:
            self._setup_database()
            self._test_can_backup_and_restore_database()
        finally:
            if self.connection:
                self.cursor.execute(TEST_DROP_CARS_TABLE_IF_EXISTS_SQL)
                self.cursor.close()
                self.connection.close()
                self._connect_without_database_name()
                self.cursor.execute(TEST_DROP_DATABASE_IF_EXISTS_SQL)
                self.connection.close()
