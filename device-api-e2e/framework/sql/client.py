import logging

import psycopg2
from psycopg2 import sql, OperationalError, InternalError

from framework.sql.helper import dsn_parse


class SQLDeviceApi:
    def __init__(self, dsn: str):
        self.pg_connection_dict = dsn_parse(dsn)
        self._init_conn()

    def _init_conn(self):
        try:
            self.conn = psycopg2.connect(**self.pg_connection_dict)
            self.cursor = self.conn.cursor()
        except OperationalError:
            logging.exception('Unable to connect to DB')

    def _make_query(self, query: sql.SQL, params=None, is_retry=False):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except (InternalError, AttributeError, OperationalError) as e:
            if not is_retry:
                logging.exception('Reconnecting...')
                self._init_conn()
                return self._make_query(query, params, is_retry=True)
            else:
                raise e

    def entries_by_id(self, device_id: int):
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
        return self._make_query(query, (device_id,))
