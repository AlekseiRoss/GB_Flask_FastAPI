from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from random import choice

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str


tasks = []
statuses = ['done', 'in progress', 'to do']
for i in range(1, 6):
    id = i
    title = 'name_' + str(i)
    description = 'description_' + str(i)
    status = choice(statuses)
    data = {'id': id, 'title': title, 'description': description,
            'status': status}
    task = Task(**data)
    tasks.append(task)
print(tasks)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/data/")
async def data_task():
    return {"tasks": tasks}


@app.post("/tasks/")
async def create_task(task: Task):
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}/")
async def update_task(task_id: int, task: Task):
    for index, t in enumerate(tasks):
        if t.id == task_id:
            print(index)
            tasks[index] = task
            return {"task_id": task_id, "task": task}
    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
    return {"task_id": task_id}
