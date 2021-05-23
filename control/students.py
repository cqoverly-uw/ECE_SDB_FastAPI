from typing import List

from connect import get_cursor
import sql_scripts


def get_student_data(sql: str, sid: str) -> dict:

    cursor = get_cursor()
    cursor.execute(sql, sid)
    data = [s for s in cursor][0]

    # parse data into student attributes
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


def get_student_current_schedule(sid: int) -> list:
    sql = sql_scripts.student_current_schedule_query
    cursor = get_cursor()
    cursor.execute(sql, sid)
    data = [c for c in cursor]
    return data


def get_student_transcript(sid: int) -> list:
    sql = sql_scripts.student_transcript_query
    cursor = get_cursor()
    cursor.execute(sql, sid)
    data = [course for course in cursor]
    return data


def get_current_ee_undergrads_data(sql: str) -> List[tuple]:
    cursor = get_cursor()
    cursor.execute(sql)
    student_data = [s for s in cursor]

    return student_data


