import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from api.deps import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_db():
    from db.base_class import Base
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_task():
    return {
        "title": "Test Task",
        "description": "Test Description",
        "status": "todo"
    }


def test_create_task(test_db, sample_task):
    response = client.post("/tasks/", json=sample_task)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_task["title"]
    assert data["description"] == sample_task["description"]
    assert data["status"] == sample_task["status"]
    assert "id" in data
    assert "created_at" in data


def test_read_tasks(test_db, sample_task):
    client.post("/tasks/", json=sample_task)

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == sample_task["title"]


def test_read_tasks_with_status_filter(test_db, sample_task):
    client.post("/tasks/", json=sample_task)
    client.post("/tasks/", json={**sample_task, "status": "in_progress"})

    response = client.get("/tasks/?status=todo")
    assert response.status_code == 200
    data = response.json()
    assert all(task["status"] == "todo" for task in data)


def test_read_single_task(test_db, sample_task):
    create_response = client.post("/tasks/", json=sample_task)
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == sample_task["title"]


def test_read_non_existent_task(test_db):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(test_db, sample_task):
    create_response = client.post("/tasks/", json=sample_task)
    task_id = create_response.json()["id"]

    updated_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "status": "in_progress"
    }
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]
    assert data["status"] == updated_data["status"]
    assert "updated_at" in data


def test_update_non_existent_task(test_db, sample_task):
    response = client.put("/tasks/999", json=sample_task)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task(test_db, sample_task):
    create_response = client.post("/tasks/", json=sample_task)
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_non_existent_task(test_db):
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
