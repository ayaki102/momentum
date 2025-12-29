from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


# app.mount("/static", StaticFiles(directory="static"), name="static")


NAME = "name"
DATE = "date"
COMPLETED = "completed"
ID = "id"

tasks = [
    {
        NAME: "test",
        DATE: "26-12-2025 12:30",
        COMPLETED: False,
        ID: 1,
    },
    {
        NAME: "dziwko",
        DATE: "6-3-2025 12:00",
        COMPLETED: False,
        ID: 2,
    },
    {
        NAME: "praca",
        DATE: "28-2-2025 1:15",
        COMPLETED: False,
        ID: 3,
    },
]

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/task")
async def get_tasks(request: Request):
    return templates.TemplateResponse(
        request=request, name="tasks.html", context={"tasks": tasks}
    )


@app.get("/task/{id}", response_class=HTMLResponse)
async def get_task(request: Request, id: int):
    task = tasks[id - 1]
    return templates.TemplateResponse(
        request=request, name="task.html", context={"task": task}
    )


@app.post("/task/status_update/{id}")
async def complete_task(id: int):
    if id < 1 or id > len(tasks):
        return HTMLResponse(content="Task not found", status_code=404)
    if tasks[id - 1][COMPLETED]:
        tasks[id - 1][COMPLETED] = False
    else:
        tasks[id - 1][COMPLETED] = True

    return RedirectResponse(url="/task", status_code=303)
