from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from models.task import Task
from schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: TaskCreate) -> Task:
        db_task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=datetime.now()
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_tasks(
            self,
            skip: int = 0,
            limit: int = 100,
            status: Optional[str] = None
    ) -> List[Task]:
        query = self.db.query(Task)
        if status:
            query = query.filter(Task.status == status)
        return query.offset(skip).limit(limit).all()

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def update_task(self, task_id: int, task: TaskUpdate) -> Optional[Task]:
        db_task = self.get_task(task_id)
        if db_task is None:
            return None

        update_data = task.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: int) -> bool:
        db_task = self.get_task(task_id)
        if db_task is None:
            return False

        self.db.delete(db_task)
        self.db.commit()
        return True
