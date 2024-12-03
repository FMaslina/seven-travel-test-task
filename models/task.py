import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime

from db.base_class import Base


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default=TaskStatus.todo)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True)
