from typing import Generator
from sqlalchemy.orm import Session

from app.database import get_db

# Можно добавить позже, если понадобится
def get_task_crud(db: Session = Depends(get_db)):
    from app.crud import task_crud
    return task_crud