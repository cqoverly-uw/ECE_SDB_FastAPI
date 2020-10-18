import os

from fastapi import params
import pyodbc
import sys
from pathlib import Path

import preferences


server = r'edwpub.s.uw.edu'
database = r'UWSDBDataStore'

## Users must add a file a the same level as this module. Name the file 'preferences.py' and add:
## USERNAME = 'NETID\<your username>'
## PWD = '<your password>'
username = preferences.USERNAME
password = preferences.PWD



def get_cursor():

    if os.name != 'posix':
        try:
            # print('Looking for usable DSN')
            conn = pyodbc.connect('DSN=EDW')
        except pyodbc.OperationalError:
            try:
                print('DSN unavailable. Trying to use mssql driver.')
                conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=edwpub.s.uw.edu;DATABASE=UWSDBDataStore;UID='+username+';PWD='+password+';')
            except:
                print('UNABLE TO CONNECT')
    else:
        
        try:
            # print('No usable mssql driver. Attempting to connect via FreeTDS')
            # db = input('Enter database name: ')
            conn = pyodbc.connect('DRIVER={FreeTDS};SERVER=edwpub.s.uw.edu; PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password+';')
        except pyodbc.OperationalError:
            print("Not able to connect with provided methods")
            sys.exit()
        # finally:
        #     conn.close()

    # print('Connection to database successful')
    return conn.cursor()


def run_query(sql):
    cursor = get_cursor()
    cursor.execute(sql, sid)
    data = [s for s in cursor]
    return data
            

def get_student_data(sql: str, sid: str)-> dict:

    cursor = get_cursor()
    cursor.execute(sql, sid)
    data = [s for s in cursor][0]

    #parse data into student attributes
    student_no = data[0]
    split_name = data[1].split(sep=',')
    last_name, first_name = split_name[0], split_name[1]
    pref_first_name = data[2].strip()
    qtrs_used = data[3]
    uw_email = data[4]
    alt_email = data[5]
    campus = data[6]
    major_abbr = data[7]
    deg_pathway = data[8]
    deg_level = data[9]
    deg_type = data[10]
    deg_status = data[11]
    deg_earned_yr = data[12]
    deg_earned_qtr = data[13]

    if pref_first_name:
        first_name = pref_first_name

    # package data for injection into template
    student_info = {
            "sid": student_no,
            "name": f'{first_name} {last_name}',
            "qtrs_used": qtrs_used,
            "uw_email": uw_email,
            "other_email": alt_email,
            "campus": campus,
            "major": major_abbr,
            "degree": f'{deg_pathway}-{deg_level}{deg_type}',
            "degree_status": deg_status,
            "degree_earned": f'{deg_earned_qtr}-{deg_earned_yr}'
    }

    return student_info


def get_course_info(sql, course_paramters):
    cursor = get_cursor()
    cursor.execute(sql, course_paramters)
    data = [s for s in cursor]

    return {"course_data": data}

if __name__ == '__main__':
    cur = get_cursor('UWSDBDataStore')
    cur.execute("SELECT 'YES'")