import uvicorn

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from starlette.routing import request_response

from views import courses
from views import faculty
from views import home
from views import students
from views import rooms

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def main():
    configure(dev_mode=True)
    uvicorn.run(app, host="127.0.0.7", port=8000, debug=True)


def configure(dev_mode: bool):
    configure_routes()


def configure_templates():
    pass


def configure_routes():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(courses.router)
    app.include_router(faculty.router)
    app.include_router(home.router)
    app.include_router(students.router)
    app.include_router(rooms.router)


if __name__ == "__main__":
    main()
else:
    configure(dev_mode=False)
