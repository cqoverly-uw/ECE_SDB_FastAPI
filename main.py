import typing

from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.routing import request_response

import sql_scripts
import connect

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return(templates.TemplateResponse("index.html", {"request": request}))

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id:str):
    return(templates.TemplateResponse("item.html", {"request": request, "id": id}))


@app.get("/student_info/", response_class=HTMLResponse)
async def get_student_info_from_sid(request: Request, sid: Optional[str]=None):
    sql: str = None
    if sid:
        if '@' not in sid:
            print('Student Number Search')
            sql = sql_scripts.info_from_sid
        elif '@uw.edu' in sid:
            print('UW Email Search')
            sql = sql_scripts.student_from_uw_email
        else:
            print("Other Search")
            sql = sql_scripts.student_from_alt_email
        student_info = connect.get_student_data(sql, sid)
        student_info["request"] = request
        return(templates.TemplateResponse("student_info.html", student_info))
    else:
        return(templates.TemplateResponse("student_info.html", {"request":request}))
    

@app.get("/course_history", response_class=HTMLResponse)
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

        course_info: dict = connect.get_course_info(sql,
                (
                    int(start),
                    int(end),
                    dept,
                    int(number)
            )
        )
        course_info['request']=request

        return(templates.TemplateResponse("course_info.html", course_info))
    else:
        return(templates.TemplateResponse("course_info.html", {'request':request}))


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
        fac_crs_history_data = connect.get_fac_crs_info(sql, 
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


@app.get("/facutly_code/", response_class=HTMLResponse)
async def get_faculty_code(
        request: Request,
        fac_name: Optional[str]=None,
        code_yr: Optional[str]=None,
        code_qtr: Optional[str]=None
    ):
    
    if fac_name and code_yr and code_qtr:
        sql = sql_scripts.faculty_code_query
        fac_name += '%'
        fac_code_info = connect.get_faculty_code(sql,
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
    sql = sql_scripts.faculty_list_query
    data = connect.get_faculty_list(sql)
    faculty_list_info = {
        'request': request,
        'instructor_list': data
    }
    return(templates.TemplateResponse("faculty_list.html", faculty_list_info))