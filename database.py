import os
import sqlite3
import pyodbc

import sys

import preferences
import connect

class Database:

    def __init__(self, db_type: str, server: str, username: str, password: str):
        self.db_type = db_type
        self.server = server
        self.username = username
        self.password = password

    def get_connection(self):
        if self.db_type == "mssql":
            # conn = pyodbc.connect(f"DSN={self.server}"
            # return conn
            return connect.get_cursor()

        elif self.db_type == "sqlite3":
            conn = sqlite3.connect(self.server)
            return conn.cursor()

    # def get_cursor(self):
    #     conn = self.get_connection()
    #     cur = conn.cursor()
    #     return cur



if __name__ == "__main__":
    sql = """
        SELECT TOP 10 *
        FROM sec.sr_instructor i
    """
    msdb = Database("mssql", "EDW", "NETID\cqoverly", "12rover12")
    cur = msdb.get_connection()
    cur.execute(sql)
    for r in cur:
        print(r)
