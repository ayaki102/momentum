from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles  # noqa: F401
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


@app.get("/dashboard")
async def get_tasks(request: Request):
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"tasks": tasks}
    )


@app.get("/task/{id}", response_class=HTMLResponse)
async def get_task(request: Request, id: int):
    task = next((t for t in tasks if t[ID] == id), None)

    if not task:
        return HTMLResponse("task not found", status_code=404)
    return templates.TemplateResponse(
        request=request, name="task.html", context={"task": task}
    )


@app.post("/task/status_update/{id}")
async def complete_task(id: int, request: Request):
    task = next((t for t in tasks if t[ID] == id), None)

    if not task:
        return HTMLResponse("Task not found", status_code=404)

    task[COMPLETED] = not task[COMPLETED]

    next_url = request.query_params.get("next", "/task")
    return RedirectResponse(next_url, status_code=303)


@app.post("/task/create")
async def create_task(
    name: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
):
    new_task = {
        NAME: name,
        DATE: f"{date} {time}",
        COMPLETED: False,
        ID: len(tasks) + 1,
    }

    tasks.append(new_task)
    return RedirectResponse(url="/task", status_code=303)


@app.post("/task/delete/{id}")
async def delete_task(id: int, request: Request):
    for i, task in enumerate(tasks):
        if task[ID] == id:
            tasks.pop(i)
            break

    next_url = request.query_params.get("next", "/task")
    return RedirectResponse(url=next_url, status_code=303)
