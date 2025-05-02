from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from schemas.column import ColumnInfo, ColumnCreate, ColumnUpdate
from models.column import Column
from db import Database

router = APIRouter(tags=["columns"])

@router.post("/", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_column(data: ColumnCreate):
    with Database() as db:
        column = Column(
            title=data.title,
            project_id=data.project_id,
            order=data.order
        )
        db.add(column)
        db.commit()
        return column.id

@router.get("/{column_id}", response_model=ColumnInfo)
async def get_column(column_id: int):
    with Database() as db:
        column = db.scalar(select(Column).where(Column.id == column_id))
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")
        return column

@router.patch("/{column_id}", response_model=ColumnInfo)
async def update_column(column_id: int, data: ColumnUpdate):
    with Database() as db:
        column = db.scalar(select(Column).where(Column.id == column_id))
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")
        
        if data.title is not None:
            column.title = data.title
        if data.order is not None:
            column.order = data.order
            
        db.commit()
        return column

@router.delete("/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_column(column_id: int):
    with Database() as db:
        column = db.scalar(select(Column).where(Column.id == column_id))
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")
        db.delete(column)
        db.commit()
