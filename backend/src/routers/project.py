from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from schemas.project import ProjectInfo, ProjectCreate, ProjectUpdate
from models.project import Project
from db import Database

project_router = APIRouter()

@project_router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate):
    with Database() as db:
        project = Project(
            name=data.name,
            description=data.description
        )
        db.add(project)
        db.commit()
        return project.id

@project_router.get("/{project_id}", response_model=ProjectInfo)
async def get_project(project_id: int):
    with Database() as db:
        project = db.scalar(select(Project).where(Project.id == project_id))
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

@project_router.patch("/{project_id}", response_model=ProjectInfo)
async def update_project(project_id: int, data: ProjectUpdate):
    with Database() as db:
        project = db.scalar(select(Project).where(Project.id == project_id))
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        if data.is_active is not None:
            project.is_active = data.is_active
        
        db.commit()
        return project

@project_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int):
    with Database() as db:
        project = db.scalar(select(Project).where(Project.id == project_id))
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(project)
        db.commit()
