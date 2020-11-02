from connect import get_cursor


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


def get_course_info(sql: str, search_parameters: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, search_parameters)
    data = [s for s in cursor]

    return {"course_data": data}