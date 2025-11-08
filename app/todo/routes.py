from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.lib.db_dependencies import get_db
from app.todo.models import TodoCreate, TodoUpdate, TodoOut
from app.todo import service as svc

router = APIRouter()

@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    return svc.create_todo(db, payload)

@router.get("/", response_model=list[TodoOut])
def list_todos(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return svc.list_todos(db, skip, limit)

@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return svc.get_todo(db, todo_id)

@router.patch("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    return svc.update_todo(db, todo_id, payload)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    svc.delete_todo(db, todo_id)
    return None

