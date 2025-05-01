from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ColumnCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, example="In Progress")
    project_id: int = Field(..., example=1)
    order: int = Field(..., example=1)

class ColumnInfo(BaseModel):
    id: int
    title: str
    project_id: int
    order: int
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ColumnUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    order: Optional[int] = Field(None, ge=0)
