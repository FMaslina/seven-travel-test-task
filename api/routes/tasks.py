from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.task import TaskCreate, TaskUpdate, TaskRead
from services.task_service import TaskService

router = APIRouter()


@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.create_task(task)


@router.get("/", response_model=List[TaskRead])
def read_tasks(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        db: Session = Depends(get_db)
):
    task_service = TaskService(db)
    return task_service.get_tasks(skip=skip, limit=limit, status=status)


@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    updated_task = task_service.update_task(task_id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    if not task_service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
