import os

import pyodbc
import sys
from pathlib import Path

import preferences


server = r"edwpub.s.uw.edu"
database = r"UWSDBDataStore"

# Users must add a file a the same level as this module. Name the file '
# preferences.py' and add:
# USERNAME = 'NETID\<your username>'
# PWD = '<your password>'
username = preferences.USERNAME
password = preferences.PWD



def get_cursor():

    if os.name != "posix":
        try:
            # print('Looking for usable DSN')
            conn = pyodbc.connect("DSN=EDW")
        except pyodbc.OperationalError:
            try:
                print("DSN unavailable. Trying to use mssql driver.")
                conn = pyodbc.connect(
                    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=edwpub.s.uw.edu;DATABASE=UWSDBDataStore;UID="
                    + username
                    + ";PWD="
                    + password
                    + ";"
                )
            except BaseException as e:
                print("UNABLE TO CONNECT")
                print(e)
    else:

        try:
            print("No usable mssql driver. Attempting to connect via FreeTDS")
            # db = input("Enter database name: ")
            conn = pyodbc.connect(
                f"DSN=EDW;DATABASE={database};UID={username};PWD={password};"
            )

            # conn = pyodbc.connect(
            #     "DSN=uwsdb;DATABASE="
            #     + database
            #     + ";UID="
            #     + username
            #     + ";PWD="
            #     + password
            #     + ";"
            # )
            print("Connected with FreeTDS DSN method")

        except pyodbc.InterfaceError:
            odbc_driver_path = preferences.ODBCDRIVER
            conn = pyodbc.connect(
                "DRIVER="
                + odbc_driver_path
                + ";SERVER=edwpub.s.uw.edu; PORT=1433;DATABASE="
                + database
                + ";UID="
                + username
                + ";PWD="
                + password
                + ";"
            )
            print("Connected with direct driver method!")
        except pyodbc.OperationalError:
            print("Not able to connect with provided methods")
            sys.exit()
        # finally:
        #     conn.close()

    # print('Connection to database successful')
    return conn.cursor()


if __name__ == "__main__":
    cur = get_cursor()
    cur.execute("SELECT TOP 1 student_name_lowc FROM sec.student_1")
    for i in cur:
        print(i)
