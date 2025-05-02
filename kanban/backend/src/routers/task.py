from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from schemas.task import TaskInfo, TaskCreate, TaskUpdate
from models.task import Task
from db import Database
from models.project import Project
from models.column import Column
router = APIRouter()

@router.post("/", response_model=int)
async def create_task(data: TaskCreate):
    with Database() as db:
        project = db.scalar(select(Project).where(Project.id == data.project_id))
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if data.column_id:
            column = db.scalar(select(Column).where(Column.id == data.column_id))
            if not column:
                raise HTTPException(status_code=404, detail="Column not found")
            if column.project_id != data.project_id:
                raise HTTPException(status_code=400, detail="Column doesn't belong to project")

        task = Task(
            title=data.title,
            description=data.description,
            project_id=data.project_id,
            column_id=data.column_id
        )
        db.add(task)
        db.commit()
        return task.id

@router.get("/{task_id}", response_model=TaskInfo)
async def get_task(task_id: int):
    with Database() as db:
        task = db.scalar(select(Task).where(Task.id == task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    
@router.get("/project/{project_id}", response_model=list[TaskInfo])
async def get_project_tasks(project_id: int):
    with Database() as db:
        tasks = db.scalars(
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(Task.created_at.desc())
        ).all()
        return tasks

@router.patch("/{task_id}", response_model=TaskInfo)
async def update_task(task_id: int, data: TaskUpdate):
    with Database() as db:
        task = db.scalar(select(Task).where(Task.id == task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.completed is not None:
            task.completed = data.completed
        
        db.commit()
        return task

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    with Database() as db:
        task = db.scalar(select(Task).where(Task.id == task_id))
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(task)
        db.commit()
