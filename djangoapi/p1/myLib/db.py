
import psycopg
from psycopg.rows import dict_row
from p1.myLib import p1Settings


class Db:
    def __init__(self, use_dict_rows=True):
        self.conn = psycopg.connect(
            dbname=p1Settings.POSTGRES_DB,
            user=p1Settings.POSTGRES_USER,
            password=p1Settings.POSTGRES_PASSWORD,
            host=p1Settings.POSTGRES_HOST,
            port=p1Settings.POSTGRES_PORT
        )
        if use_dict_rows:
            self.cur = self.conn.cursor(row_factory=dict_row)
        else:
            self.cur = self.conn.cursor()

    def query(self, sql, params=None):
        self.cur.execute(sql, params or [])
        return self.cur.fetchall()

    def execute(self, sql, params=None):
        self.cur.execute(sql, params or [])
        self.conn.commit()
        return self.cur.rowcount

    def close(self):
        self.cur.close()
        self.conn.close()