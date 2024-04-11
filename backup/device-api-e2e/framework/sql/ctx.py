import psycopg2
from psycopg2 import sql

from config import DSN
from framework.sql.helper import dsn_parse


class DBCtx:
    def __init__(self, dsn):
        self.conn = psycopg2.connect(**dsn_parse(dsn))
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def make_query(self, query: sql.SQL, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()


def entries_by_id(device_id: int):
    query = sql.SQL("SELECT {fields} FROM {table} WHERE device_id = %s").format(
        fields=sql.SQL(',').join([
            sql.Identifier('device_id'),
            sql.Identifier('type'),
            sql.Identifier('status'),
            sql.Identifier('payload'),
            sql.Identifier('created_at'),
            sql.Identifier('updated_at'),
        ]),
        table=sql.Identifier('devices_events')
    )
    with DBCtx(DSN) as db:
        return db.make_query(query, (device_id,))
