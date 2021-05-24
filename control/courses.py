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
                "dept": row[0].strip(),
                "joint_courses": [],
                "resp_dept": row[4],
            }
    for row in joint_course_data:
        course_no = row[1]
        course_joins_info[course_no]["joint_courses"].append(f"{row[2]} {row[3]}")

    return course_joins_info


def get_course_history(sql: str, search_parameters: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, search_parameters)
    data = [s for s in cursor]

    return {"course_data": data}


def get_single_course_info(sql: str, params: tuple) -> dict:
    cursor = get_cursor()
    cursor.execute(sql, params)
    try:
        data = [info for info in cursor][0]
        base_info = {
            "dept": data[0],
            "crs_number": data[1],
            "min_credits": data[2],
            "max_credits": data[3],
            "credit_ctrl": data[4],
            "grade_sys": data[5],
            "short_title": data[6],
            "long_title": data[7],
            "resp_crs": data[8],
            "diversity": data[9],
            "i_and_s": data[10],
            "vis_lit_perf_arts": data[11],
            "eng_comp": data[12],
            "writing": data[13],
        }
    except IndexError:
        return {}
    return base_info


def get_course_prereqs(sql: str, params: tuple) -> list:
    prereqs = None
    cursor = get_cursor()
    cursor.execute(sql, params)
    try:
        prereqs = [p for p in cursor]
        return prereqs
    except IndexError:
        return []


def get_is_prereq_for(sql: str, params: tuple) -> list:
    prereq_for: list = None
    cursor = get_cursor()
    cursor.execute(sql, params)
    try:
        prereq_for = [p for p in cursor]
        return prereq_for
    except IndexError:
        return []


def get_single_course_joins(sql: str, params: tuple) -> list:
    cursor = get_cursor()
    cursor.execute(sql, params)
    joined_courses = [c[0] for c in cursor]

    if joined_courses:
        return joined_courses
    else:
        return ["None"]
