from sqlalchemy import Column, Integer, String, Boolean, DateTime 
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    tasks = relationship("Task", backref="project")  # Связь один-ко-многим
    columns = relationship("Column", backref="project")
