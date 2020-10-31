import os
from typing import List

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
    # cum_gpa = data[11]
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


def get_course_info(sql: str, search_parameters: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, search_parameters)
    data = [s for s in cursor]

    return {"course_data": data}


def get_fac_crs_info(sql: str, search_parameters: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, search_parameters)
    data = [s for s in cursor]

    return {"fac_crs_history_data": data}


def get_faculty_code(sql: str, search_parameters: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, search_parameters)
    data = [s for s in cursor][0]
    fac_code_data = {
        'fac_eid': data[0],
        'fac_name': data[1],
        'code_yr': data[2],
        'code_qtr': data[3],
        'fac_code': data[4]
    }
    return fac_code_data


def get_faculty_list(sql: str, year: int) -> List[tuple]:
    cursor = get_cursor()
    cursor.execute(sql, year)
    instructor_list_info = [i for i in cursor]
    return instructor_list_info


def get_joint_course_data(sql: str) -> dict:
    course_joins_info = {}
    cursor = get_cursor()
    cursor.execute(sql)
    joint_course_data = [c for c in cursor]
    for row in joint_course_data:
        course_no = row[1]
        if course_no not in course_joins_info.keys():
            course_joins_info[course_no] = {
                    'dept': row[0].strip(),
                    'joint_courses': [],
                    'resp_dept': row[4]
            }
    for row in joint_course_data:
        course_no = row[1]
        course_joins_info[course_no]['joint_courses'].append(f'{row[2]} {row[3]}')

    return course_joins_info


def get_current_ee_undergrads_data(sql: str) -> List[tuple]:
    cursor = get_cursor()
    cursor.execute(sql)
    student_data = [s for s in cursor]

    return student_data


if __name__ == '__main__':
    cur = get_cursor('UWSDBDataStore')
    cur.execute("SELECT 'YES'")