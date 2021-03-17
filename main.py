import typing
from typing import Optional, List
from datetime import datetime

from fastapi import FastAPI, Request, Query 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.routing import request_response

import sql_scripts
import students
import courses
import faculty

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return(templates.TemplateResponse("index.html", {"request": request}))

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id:str):
    return(templates.TemplateResponse("item.html", {"request": request, "id": id}))

##### HTTP calls for information regarding students ####
@app.get("/student_info/", response_class=HTMLResponse)
async def get_student_info_from_sid(request: Request, sid: Optional[str]=Query(None)):
    sql: str = None
    student_info = None
    schedule = []
    if sid:
        if '@' not in sid:
            sql = sql_scripts.info_from_sid
        elif '@uw.edu' in sid:
            sql = sql_scripts.student_from_uw_email
        else:
            sql = sql_scripts.student_from_alt_email
        student_info = students.get_student_data(sql, sid)
        try:
            student_no = student_info["sid"]
            schedule_sql = sql_scripts.student_current_schedule_query
            schedule = students.get_student_current_schedule(schedule_sql, student_no)
            formatted_schedule = []
            for c in schedule:
                s = f"{c[0]}-{c[1]} | {c[2]} | {c[3]} {c[4]}{c[5]} | {c[6]}cr. | {c[7]}"
                formatted_schedule.append(s)
            student_info['current_schedule'] = formatted_schedule
        except KeyError as e:
            pass
        student_info["request"] = request

        return(templates.TemplateResponse("student_info.html", student_info))
    else:
        return(templates.TemplateResponse("student_info.html", {"request":request}))
    

@app.get("/current_ee_undergrads.html/", response_class=HTMLResponse)
async def get_current_ee_undergrads(request: Request):
    sql: str = sql_scripts.current_ee_undergrads_query
    data: List[tuple] = students.get_current_ee_undergrads_data(sql)
    undergrad_info = {
        'request': request,
        'student_list': data
    }

    return(templates.TemplateResponse("current_ee_undergrads.html", undergrad_info))


##### HTTP calls for information regarding courses ####

@app.get("/course_info/", response_class=HTMLResponse)
async def get_course_info(
        request: Request,
        dept: Optional[str]=Query(None, max_length=6),
        crs_number: Optional[int]=Query(None)):
    sql_base_info = sql_scripts.single_course_info
    sql_joins = sql_scripts.single_course_joins_info
    sql_prereqs = sql_scripts.course_prereqs_query
    sql_prereq_for = sql_scripts.course_is_prereq_for_query
    if dept and crs_number: 
        course_base_info: dict = courses.get_single_course_info(
            sql_base_info,
            (dept, crs_number)
        )
        joined_courses: list = courses.get_single_course_joins(
            sql_joins,
            (dept, crs_number)
        )
        prereqs: list = courses.get_course_prereqs(
            sql_prereqs,
            (dept, crs_number)
        )
        # prereq_for: list = courses.get_is_prereq_for(
        #     sql_prereq_for,
        #     (dept, crs_number)
        # )
        full_course_info = {
            'request': request,
            'joined_courses': joined_courses,
            'prereqs': prereqs,
            **course_base_info
        }
        return(templates.TemplateResponse("course_info.html", full_course_info)) 
    else:
        return(templates.TemplateResponse("course_info.html", {'request': request}))


@app.get("/course_history/", response_class=HTMLResponse)
async def get_course_history(
        request: Request,
        dept: Optional[str]=None,
        number: Optional[str]=None,
        start: Optional[str]=None,
        end: Optional[str]=None
    ):
    # dept = dept_abbr
    # number = crs_no
    # start = start_yr
    # end = end_yr

    if dept and number and start and end:
        sql = sql_scripts.course_history

        course_history: dict = courses.get_course_history(sql,
                (
                    int(start),
                    int(end),
                    dept,
                    int(number)
            )
        )
        course_history['request']=request
        course_history['start']=start
        course_history['end']=end

        return(templates.TemplateResponse("course_history.html", course_history))
    else:
        return(templates.TemplateResponse("course_history.html", {'request':request}))


@app.get("/joint_courses.html/", response_class=HTMLResponse)
async def get_joint_course_list(request: Request):
    sql: str = sql_scripts.joint_courses_query
    data: dict = courses.get_joint_course_data(sql)
    joint_courses_info = {
        'request': request,
        'joint_courses_data': data
    }

    return(templates.TemplateResponse("joint_courses.html", joint_courses_info))


##### HTTP calls for information regarding facutly ####
@app.get("/fac_crs_history/", response_class=HTMLResponse)
async def get_fac_crs_history(
        request:Request,
        fac_name: Optional[str]=None,
        start_yr: Optional[str]=None,
        end_yr: Optional[str]=None,
    ):
    
    if fac_name and start_yr and end_yr:
        print('SHOULD BE RUNNING QUERY')
        sql = sql_scripts.fac_crs_history_query
        fac_name += '%'
        fac_crs_history_data = faculty.get_fac_crs_info(sql, 
                (
                    int(start_yr),
                    int(end_yr),
                    fac_name
            )
        )
        fac_crs_history_data['request'] = request
        return(templates.TemplateResponse("faculty_crs_history.html", fac_crs_history_data))

    else:
        return(templates.TemplateResponse("faculty_crs_history.html", {'request':request}))


@app.get("/faculty_code/", response_class=HTMLResponse)
async def get_faculty_code(
        request: Request,
        fac_name: Optional[str]=None,
        code_yr: Optional[str]=None,
        code_qtr: Optional[str]=None
    ):
    
    if fac_name and code_yr and code_qtr:
        sql = sql_scripts.faculty_code_query
        fac_name += '%'
        fac_code_info = faculty.get_faculty_code(sql,
                (
                        fac_name,
                        int(code_yr),
                        int(code_qtr)
            )
        )
        fac_code_info['request'] = request
        return(templates.TemplateResponse("faculty_code.html", fac_code_info))

    else:
        return(templates.TemplateResponse("faculty_code.html", {'request': request}))


@app.get("/faculty_list/", response_class=HTMLResponse)
async def get_faculty_list(request: Request):
    year: int = datetime.now().date().year
    sql: str = sql_scripts.faculty_list_query
    data: List[tuple] = faculty.get_faculty_list(sql, year)
    faculty_list_info = {
        'request': request,
        'instructor_list': data
    }
    return(templates.TemplateResponse("faculty_list.html", faculty_list_info))



