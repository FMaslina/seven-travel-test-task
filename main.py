from fastapi import FastAPI

from core.config import settings
from api.routes import tasks

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(tasks.router, prefix='/tasks', tags=['tasks'])
