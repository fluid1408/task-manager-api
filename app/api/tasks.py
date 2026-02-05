from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas, models

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=schemas.PaginatedResponse)
def read_tasks(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    status: Optional[schemas.TaskStatus] = Query(None, description="Фильтр по статусу"),
    priority: Optional[schemas.TaskPriority] = Query(None, description="Фильтр по приоритету"),
    search: Optional[str] = Query(None, description="Поиск по названию или описанию"),
):
    """
    Получить список задач с пагинацией и фильтрацией.
    
    - **page**: Номер страницы (начинается с 1)
    - **page_size**: Количество задач на странице (1-100)
    - **status**: Фильтр по статусу (active/completed/pending)
    - **priority**: Фильтр по приоритету (low/medium/high)
    - **search**: Поиск по названию или описанию
    """
    skip = (page - 1) * page_size
    
    tasks, total = crud.task_crud.get_multi(
        db,
        skip=skip,
        limit=page_size,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        search=search
    )
    
    return {
        "items": tasks,
        "total": total,
        "page": page,
        "pages": (total + page_size - 1) // page_size if total > 0 else 0,
        "page_size": page_size
    }

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить задачу по ID.
    """
    task = crud.task_crud.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return task

@router.post("/", 
             response_model=schemas.TaskResponse,
             status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую задачу.
    """
    return crud.task_crud.create(db, obj_in=task_in)

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить существующую задачу.
    """
    task = crud.task_crud.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    return crud.task_crud.update(db, db_obj=task, obj_in=task_in)

@router.delete("/{task_id}", response_model=schemas.TaskResponse)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить задачу (мягкое удаление).
    """
    task = crud.task_crud.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    return crud.task_crud.delete(db, id=task_id)