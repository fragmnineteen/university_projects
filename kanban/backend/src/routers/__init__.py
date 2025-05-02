from fastapi import APIRouter
from routers.task import router as task_router
from routers.project import project_router  # Изменили здесь
from routers.column import router as column_router

router = APIRouter(prefix="/api/v1")
router.include_router(task_router, prefix="/tasks", tags=["Tasks"])
router.include_router(project_router, prefix="/projects", tags=["Projects"])
router.include_router(column_router, prefix="/columns")