import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Основные
    PROJECT_NAME: str = "Task Manager API"
    
    # База данных
    DATABASE_URL: str = "sqlite:///./tasks.db"
    
    # Пагинация
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"

settings = Settings()