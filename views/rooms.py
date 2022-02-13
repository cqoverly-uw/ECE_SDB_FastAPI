from typing import Optional, List

# from datetime import datetime

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse

# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import tablesample

# from starlette.routing import request_response

import sql_scripts

from control import rooms


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/room_info/", response_class=HTMLResponse)
async def get_room_info(
    request: Request,
    bldg: Optional[str] = None,
    room_no: Optional[str] = None
):
    if bldg and room_no:
        sql = sql_scripts.get_room_attributes
        room_info = rooms.get_room_attrs(sql, (bldg, room_no))
        room_info["request"] = request
        return templates.TemplateResponse(
            "rooms/room_info.html", room_info
        )

    else:
        return templates.TemplateResponse("rooms/room_info.html", {"request": request})
