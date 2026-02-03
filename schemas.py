from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool


class TaskResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True
