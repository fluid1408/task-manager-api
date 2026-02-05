# В app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.database import engine, Base
from app.api.tasks import router as tasks_router  # Импортируем напрямую

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="Простой менеджер задач с фронтендом",
    version="1.0.0"
)

# Подключаем tasks роутер напрямую с префиксом
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Task Manager API"}

@app.get("/api/v1/tasks/") 
def test_endpoint():
    return {"message": "API работает!"}