from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import sql_scripts
import connect

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
        student_info = connect.get_student_data(sql, sid)
        student_info["request"] = request

        return(templates.TemplateResponse("student_info.html", student_info))
    else:
        return(templates.TemplateResponse("student_info.html", {"request":request}))
    
