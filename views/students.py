from typing import Optional, List

# from datetime import datetime

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse

# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from starlette.routing import request_response

import sql_scripts

from control import students


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# #### HTTP calls for information regarding students ####
@router.get("/student_info/", response_class=HTMLResponse)
async def get_student_info_from_sid(request: Request, sid: Optional[str] = Query(None)):
    sql: str = None
    student_info = None
    schedule = []

    # get general student information based on student no. or email address
    if sid:
        if "@" not in sid:
            sql = sql_scripts.info_from_sid
        elif "@uw.edu" in sid:
            sql = sql_scripts.student_from_uw_email
        else:
            sql = sql_scripts.student_from_alt_email
        try:
            student_info = students.get_student_data(sql, sid)
        except Exception as e:
            return templates.TemplateResponse(
                "students/student_info.html", {"request": request}
            )

        # if student was returned, get current schedule base in returned student no.
        try:
            student_no = student_info["sid"]
            schedule = students.get_student_current_schedule(student_no)
            formatted_schedule = []
            for c in schedule:
                qtr_yr = f"{c[0]}-{c[1]}"
                sln = c[2]
                course = f"{c[3]} {c[4]}{c[5]}"
                credits = c[6]
                instr = c[7]
                formatted_schedule.append((qtr_yr, sln, course, credits, instr))
            student_info["current_schedule"] = formatted_schedule
        except KeyError as e:  # no schedule is returned
            pass

        # if a student was retured, get the transcript
        try:
            student_no = student_info["sid"]
            transcript_data = students.get_student_transcript(student_no)
            student_info["transcript"] = transcript_data
        except KeyError as e:  # no transcript
            pass
        student_info["request"] = request

        return templates.TemplateResponse("students/student_info.html", student_info)
    else:
        return templates.TemplateResponse(
            "students/student_info.html", {"request": request}
        )


@router.get("/current_ee_undergrads.html/", response_class=HTMLResponse)
async def get_current_ee_undergrads(request: Request):
    sql: str = sql_scripts.current_ee_undergrads_query
    data: List[tuple] = students.get_current_ee_undergrads_data(sql)
    undergrad_info = {"request": request, "student_list": data}

    return templates.TemplateResponse(
        "students/current_ee_undergrads.html", undergrad_info
    )
