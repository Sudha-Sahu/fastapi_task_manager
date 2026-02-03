from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Task, SessionLocal, engine
from schemas import TaskCreate, TaskResponse

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Routes ----------------

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description, completed=task.completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = not task.completed
    db.commit()
    db.refresh(task)
    return task





















# from fastapi import FastAPI, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from pydantic import BaseModel
# from bson import ObjectId
#
# app = FastAPI()
#
# # MongoDB connection
# client = AsyncIOMotorClient("mongodb://localhost:27017")
# db = client.taskdb
#
# # Pydantic model
# class Task(BaseModel):
#     task_id: str
#     title: str
#     description: str
#     completed: bool = False
#
# @app.post("/tasks")
# async def create_task(task: Task):
#     result = await db.tasks.insert_one(task.model_dump())
#     return {"id": str(result.inserted_id), **task.model_dump()}
#
# @app.get("/tasks")
# async def list_tasks():
#     tasks = []
#     async for task in db.tasks.find():
#         task["_id"] = str(task["_id"])
#         tasks.append(task)
#     return tasks
#
# @app.put("/tasks/{task_id}")
# async def toggle_task(task_id: str):
#     result = await db.tasks.find_one({"task_id": task_id})
#     if not result:
#         raise HTTPException(status_code=404, detail="Task not found")
#     new_status = not result["completed"]
#     await db.tasks.update_one({"task_id": task_id}, {"$set": {"completed": new_status}})
#     return {"message": "Task updated", "completed": new_status}
