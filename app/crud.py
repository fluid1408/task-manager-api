from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app import models, schemas

class TaskCRUD:
    def __init__(self, model):
        self.model = model
    
    # Базовые операции
    def get(self, db: Session, id: int) -> Optional[models.Task]:
        return db.query(self.model).filter(
            self.model.id == id, 
            self.model.is_deleted == False
        ).first()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[models.Task], int]:
        
        query = db.query(self.model).filter(self.model.is_deleted == False)
        
        # Фильтры
        if status:
            query = query.filter(self.model.status == status)
        
        if priority:
            query = query.filter(self.model.priority == priority)
        
        # Поиск
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    self.model.title.ilike(search_term),
                    self.model.description.ilike(search_term)
                )
            )
        
        # Получаем общее количество ДО пагинации
        total = query.count()
        
        # Пагинация и сортировка
        items = query.order_by(
            self.model.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return items, total
    
    def create(self, db: Session, *, obj_in: schemas.TaskCreate) -> models.Task:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: models.Task, 
        obj_in: schemas.TaskUpdate
    ) -> models.Task:
        
        update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: int) -> models.Task:
        db_obj = self.get(db, id=id)
        if not db_obj:
            return None
        
        db_obj.is_deleted = True  # Мягкое удаление
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def hard_delete(self, db: Session, *, id: int) -> models.Task:
        db_obj = self.get(db, id=id)
        if not db_obj:
            return None
        
        db.delete(db_obj)
        db.commit()
        return db_obj

# Экземпляр для использования
task_crud = TaskCRUD(models.Task)