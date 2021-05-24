import typing
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.routing import request_response

import sql_scripts
from control import courses


router = APIRouter()

templates = Jinja2Templates(directory="templates")

##### HTTP calls for information regarding courses ####


@router.get("/course_info/", response_class=HTMLResponse)
async def get_course_info(
    request: Request,
    dept: Optional[str] = Query(None, max_length=6),
    crs_number: Optional[int] = Query(None),
):
    sql_base_info = sql_scripts.single_course_info
    sql_joins = sql_scripts.single_course_joins_info
    sql_prereqs = sql_scripts.course_prereqs_query
    sql_prereq_for = sql_scripts.course_is_prereq_for_query
    if dept and crs_number:
        course_base_info: dict = courses.get_single_course_info(
            sql_base_info, (dept, crs_number)
        )
        joined_courses: list = courses.get_single_course_joins(
            sql_joins, (dept, crs_number)
        )
        prereqs: list = courses.get_course_prereqs(sql_prereqs, (dept, crs_number))
        # prereq_for: list = courses.get_is_prereq_for(
        #     sql_prereq_for,
        #     (dept, crs_number)
        # )
        full_course_info = {
            "request": request,
            "joined_courses": joined_courses,
            "prereqs": prereqs,
            **course_base_info,
        }
        return templates.TemplateResponse("courses/course_info.html", full_course_info)
    else:
        return templates.TemplateResponse(
            "courses/course_info.html", {"request": request}
        )


@router.get("/course_history/", response_class=HTMLResponse)
async def get_course_history(
    request: Request,
    dept: Optional[str] = None,
    number: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
):
    # dept = dept_abbr
    # number = crs_no
    # start = start_yr
    # end = end_yr

    if dept and number and start and end:
        sql = sql_scripts.course_history

        course_history: dict = courses.get_course_history(
            sql, (int(start), int(end), dept, int(number))
        )
        course_history["request"] = request
        course_history["start"] = start
        course_history["end"] = end

        return templates.TemplateResponse("courses/course_history.html", course_history)
    else:
        return templates.TemplateResponse(
            "courses/course_history.html", {"request": request}
        )


@router.get("/joint_courses.html/", response_class=HTMLResponse)
async def get_joint_course_list(request: Request):
    sql: str = sql_scripts.joint_courses_query
    data: dict = courses.get_joint_course_data(sql)
    joint_courses_info = {"request": request, "joint_courses_data": data}

    return templates.TemplateResponse("courses/joint_courses.html", joint_courses_info)
