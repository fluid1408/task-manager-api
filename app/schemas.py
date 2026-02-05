from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

# Enums
class TaskStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PENDING = "pending"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Базовые схемы
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Купить продукты")
    description: Optional[str] = Field(None, max_length=1000, example="Молоко, хлеб, яйца")
    status: TaskStatus = Field(default=TaskStatus.ACTIVE, example="active")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, example="medium")
    
    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Название не может быть пустым')
        return v.strip()

# Для создания
class TaskCreate(TaskBase):
    pass

# Для обновления
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

# Для ответа
class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True  # Заменяет orm_mode в Pydantic v2

# Для списка с пагинацией
class PaginatedResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    pages: int
    page_size: int