
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.taskdb

# Pydantic model
class Task(BaseModel):
    task_id: str
    title: str
    description: str
    completed: bool = False

@app.post("/tasks")
async def create_task(task: Task):
    result = await db.tasks.insert_one(task.model_dump())
    return {"id": str(result.inserted_id), **task.model_dump()}

@app.get("/tasks")
async def list_tasks():
    tasks = []
    async for task in db.tasks.find():
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks

@app.put("/tasks/{task_id}")
async def toggle_task(task_id: str):
    result = await db.tasks.find_one({"task_id": task_id})
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    new_status = not result["completed"]
    await db.tasks.update_one({"task_id": task_id}, {"$set": {"completed": new_status}})
    return {"message": "Task updated", "completed": new_status}
