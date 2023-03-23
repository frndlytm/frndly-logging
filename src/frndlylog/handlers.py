import logging
import sqlite3

from contextlib import contextmanager
from typing import Sequence

from . import constants


@contextmanager
def cursor(conn: sqlite3.Connection) -> sqlite3.Cursor:
    try:
        yield (cursor := conn.connect())
    finally:
        cursor.close()


class SqliteHandler(logging.Handler):
    def __init__(
        self,
        filename: str = "./var/log/log.db",
        fields: Sequence[str] = constants.DEFAULT_FIELDS
    ):
        self.filename = filename
        self.fields = fields
        self.conn = sqlite3.connect(filename)

    def setup(self):
        with cursor(self.conn) as curs:
            curs.execute(f"CREATE TABLE frndlylog ({', '.join(self.fields)})")

    def emit(self, record: logging.LogRecord):
        row = tuple(getattr(record, field) for field in self.fields)
        command = f"""
            INSERT INTO frndlylog VALUES ({', '.join(['?' for _ in range(len(row))])})
        """

        with cursor(self.conn) as curs:
            curs.execute(command, *row)
