from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from starlette.routing import request_response

import sql_scripts

from control import faculty


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# #### HTTP calls for information regarding facutly ####
@router.get("/fac_crs_history/", response_class=HTMLResponse)
async def get_fac_crs_history(
            request: Request,
            fac_name: Optional[str] = None,
            start_yr: Optional[str] = None,
            end_yr: Optional[str] = None,
        ):
    
    if fac_name and start_yr and end_yr:
        print('SHOULD BE RUNNING QUERY')
        sql = sql_scripts.fac_crs_history_query
        fac_name += '%'
        fac_crs_history_data = faculty.get_fac_crs_info(
            sql,
            (
                    int(start_yr),
                    int(end_yr),
                    fac_name
                )
            )
        fac_crs_history_data['request'] = request
        return(templates.TemplateResponse("faculty/faculty_crs_history.html", fac_crs_history_data))

    else:
        return(templates.TemplateResponse("faculty/faculty_crs_history.html", {'request':request}))


@router.get("/faculty_code/", response_class=HTMLResponse)
async def get_faculty_code(
        request: Request,
        fac_name: Optional[str] = None,
        code_yr: Optional[str] = None,
        code_qtr: Optional[str] = None,
        ):
    
    if fac_name and code_yr and code_qtr:
        sql = sql_scripts.faculty_code_query
        fac_name += '%'
        fac_code_info = faculty.get_faculty_code(
            sql,
            (
                fac_name,
                int(code_yr),
                int(code_qtr)
            )
        )
        fac_code_info['request'] = request
        return(templates.TemplateResponse("faculty/faculty_code.html", fac_code_info))

    else:
        return(templates.TemplateResponse("faculty/faculty_code.html", {'request': request}))


@router.get("/faculty_list/", response_class=HTMLResponse)
async def get_faculty_list(request: Request):
    year: int = datetime.now().date().year
    sql: str = sql_scripts.faculty_list_query
    data: List[tuple] = faculty.get_faculty_list(sql, year)
    faculty_list_info = {
        'request': request,
        'instructor_list': data
    }
    return(templates.TemplateResponse("faculty/faculty_list.html", faculty_list_info))
