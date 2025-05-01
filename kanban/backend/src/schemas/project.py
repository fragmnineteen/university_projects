from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Website Redesign")
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        example="Complete redesign of company website"
    )

class ProjectInfo(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Website Redesign")
    description: Optional[str] = Field(None, example="Project description")
    created_at: datetime = Field(..., example="2023-01-01T00:00:00")
    is_active: bool = Field(True, example=True)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=100, 
        example="Updated project name"
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        example="Updated description"
    )
    is_active: Optional[bool] = Field(
        None, 
        example=False
    )
