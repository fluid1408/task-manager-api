import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import settings

# Тестовая база данных
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    # Создаем таблицы для тестов
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем после тестов
    Base.metadata.drop_all(bind=engine)

def test_create_task(test_db):
    response = client.post(
        "/api/v1/tasks/tasks/",  
        json={
            "title": "Тестовая задача",
            "description": "Описание тестовой задачи"
        }
    )
    print(f"CREATE Response: {response.status_code}, {response.text}") 
    assert response.status_code == 201  
    data = response.json()
    assert data["title"] == "Тестовая задача"
    
    if "id" not in data:
        print(f"Available keys: {data.keys()}")
    assert "id" in data or "task_id" in data  

def test_get_tasks(test_db):
    
    client.post("/api/v1/tasks/tasks/", json={"title": "Задача 1"})  
    
    response = client.get("/api/v1/tasks/tasks/") 
    print(f"GET TASKS Response: {response.status_code}, {response.text}") 
    assert response.status_code == 200
    data = response.json()
    
   
    if isinstance(data, list):
        
        assert len(data) >= 1
    elif isinstance(data, dict):
        
        if "items" in data:
            assert len(data["items"]) >= 1
        elif "tasks" in data:
            assert len(data["tasks"]) >= 1
        elif "results" in data:
            assert len(data["results"]) >= 1

def test_get_task_by_id(test_db):
    
    create_resp = client.post("/api/v1/tasks/tasks/", json={"title": "Для поиска"})  
    task_data = create_resp.json()
    
    task_id = task_data.get("id") or task_data.get("task_id")
    assert task_id is not None
    
    response = client.get(f"/api/v1/tasks/tasks/{task_id}") 
    assert response.status_code == 200
    data = response.json()
    assert str(data.get("id") or data.get("task_id")) == str(task_id)
    assert data["title"] == "Для поиска"

def test_update_task(test_db):
    create_resp = client.post("/api/v1/tasks/tasks/", json={"title": "Старое название"}) 
    task_data = create_resp.json()
    task_id = task_data.get("id") or task_data.get("task_id")
    assert task_id is not None
    
    
    response = client.put(
        f"/api/v1/tasks/tasks/{task_id}",  
        json={"title": "Новое название", "status": "completed"}
    )
    print(f"UPDATE Response: {response.status_code}, {response.text}")  
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Новое название"
    assert data["status"] == "completed"

def test_delete_task(test_db):

    create_resp = client.post("/api/v1/tasks/tasks/", json={"title": "Для удаления"}) 
    task_data = create_resp.json()
    task_id = task_data.get("id") or task_data.get("task_id")
    assert task_id is not None
    
  
    response = client.delete(f"/api/v1/tasks/tasks/{task_id}")  
    print(f"DELETE Response: {response.status_code}, {response.text}")  
    assert response.status_code == 200
    
    
    response = client.get(f"/api/v1/tasks/tasks/{task_id}") 
    assert response.status_code == 404

