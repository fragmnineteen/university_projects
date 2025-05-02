from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .column import ColumnInfo
from .project import ProjectInfo

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    project_id: int = Field(..., example=1)
    column_id: Optional[int] = Field(None, example=1) 

class TaskInfo(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    project_id: int
    column_id: Optional[int]
    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None