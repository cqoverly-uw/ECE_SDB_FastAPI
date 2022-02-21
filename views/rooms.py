from typing import Optional, List

# from datetime import datetime

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse

# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from sqlalchemy import tablesample

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


@router.get("/room_search/", response_class=HTMLResponse)
async def get_room_availability(
    request: Request,
    min_cap: Optional[int] = None,
    max_cap: Optional[int] = None
):
    if min_cap and max_cap:
        rooms_sql = sql_scripts.sql_room_search
        found_rooms = rooms.get_rooms_by_capacity(
            rooms_sql,
            (min_cap, max_cap)
        )

        found_rooms["request"] = request
        found_rooms["min_cap"] = min_cap
        found_rooms["max_cap"] = max_cap

        return templates.TemplateResponse(
            "rooms/room_search.html", found_rooms
        )
    else:
        return templates.TemplateResponse(
            "rooms/room_search.html",
            {"request": request}
        )


@router.get("/new_room_search/", response_class=HTMLResponse)
async def find_new_room(
    request: Request,
    year: Optional[int] = None,
    quarter: Optional[int] = None,
    sln: Optional[int] = None,
    min_cap: Optional[int] = None,
    max_cap: Optional[int] = None
):

    if year and quarter and sln and min_cap and max_cap:
        sql = sql_scripts.query_find_new_room
        params = (
                    int(year),
                    int(quarter),
                    int(sln),
                    int(min_cap),
                    int(max_cap),
        )
        found_rooms = rooms.find_new_room_for_sln(sql, params)

        found_rooms["request"] = request
        found_rooms["year"] = year
        found_rooms["quarter"] = quarter
        found_rooms["sln"] = sln
        found_rooms["min_cap"] = min_cap
        found_rooms["max_cap"] = max_cap
        
        return templates.TemplateResponse(
            "rooms/new_room_search.html",
            found_rooms
        )

    else:
        return templates.TemplateResponse(
            "rooms/new_room_search.html",
            {"request": request}
        )








@router.get("/room_availability/", response_class=HTMLResponse)
async def get_room_availability(
    request: Request,
    year: Optional[int] = None,
    days: Optional[str] = None,
    qtr: Optional[int] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    min_cap: Optional[int] = None,
    max_cap: Optional[int] = None
):
    if year and qtr and days and start and end and min_cap and max_cap:
        all_rooms_sql = sql_scripts.get_rooms
        room_schedule_sql = sql_scripts.get_room_schedule
        room_avail_sql = sql_scripts.get_room_avail
        all_rooms = rooms.get_rooms(all_rooms_sql, (year, qtr))
        room_schedule = rooms.get_room_schedule(
            room_schedule_sql,
            (year, qtr)
        )
        
        room_availability = rooms.get_room_availability(
            room_avail_sql,
            (year, qtr, days, start, end, min_cap, max_cap)
        )
        return templates.TemplateResponse(
            "rooms/room_availability.html", room_availability
        )
    else:
        return templates.TemplateResponse("rooms/room_availability.html", {"request": request})