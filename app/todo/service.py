from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Sequence
from app.todo.models import Todo, TodoCreate, TodoUpdate

def create_todo(db: Session, payload: TodoCreate) -> Todo:
    # Example rule: avoid duplicate titles (case-insensitive)
    exists = db.query(Todo).filter(Todo.title.ilike(payload.title)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Todo with this title already exists")
    todo = Todo(title=payload.title, description=payload.description)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def list_todos(db: Session, skip: int = 0, limit: int = 50) -> Sequence[Todo]:
    return db.query(Todo).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int) -> Todo:
    obj = db.get(Todo, todo_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return obj

def update_todo(db: Session, todo_id: int, payload: TodoUpdate) -> Todo:
    obj = get_todo(db, todo_id)
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_todo(db: Session, todo_id: int) -> None:
    obj = get_todo(db, todo_id)
    db.delete(obj)
    db.commit()

