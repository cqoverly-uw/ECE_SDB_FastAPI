from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import sql_scripts
from connect import get_cursor

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index():
    return {
        "Tag": "Hello, World",
        "Tag 2:": "Today is a better day!"
        }


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id:str):
    for k, v in request.items():
        print(f'{k}: {v}')
    return(templates.TemplateResponse("item.html", {"request": request, "id": id}))


@app.get("/student_info/", response_class=HTMLResponse)
async def get_student_info_from_sid(request: Request, sid: str=None):
    if sid:
        sql = sql_scripts.info_from_sid
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
        deg_status = data[11]
        deg_earned_yr = data[12]
        deg_earned_qtr = data[13]

        if pref_first_name:
            first_name = pref_first_name

        # package data for injection into template
        student_info = {
                "request": request,
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
        # print(student_info)

        return(templates.TemplateResponse("student_info.html", student_info))
    else:
        return(templates.TemplateResponse("student_info.html", {"request":request}))
    
