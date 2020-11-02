from typing import List

from connect import get_cursor



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