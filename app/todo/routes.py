from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.lib.db_dependencies import get_db
from app.lib.auth_dependencies import get_current_user
from app.todo.models import TodoCreate, TodoUpdate, TodoOut, User
from app.todo import service as svc

router = APIRouter()

# All routes require authentication via get_current_user dependency

@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(
    payload: TodoCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new todo. Requires authentication."""
    return svc.create_todo(db, payload, current_user)

@router.get("/", response_model=list[TodoOut])
def list_todos(
    skip: int = 0, 
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all todos. Requires authentication."""
    return svc.list_todos(db, current_user, skip, limit)

@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific todo by ID. Requires authentication."""
    return svc.get_todo(db, todo_id, current_user)

@router.patch("/{todo_id}", response_model=TodoOut)
def update_todo(
    todo_id: int, 
    payload: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a todo. Requires authentication."""
    return svc.update_todo(db, todo_id, payload, current_user)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a todo. Requires authentication."""
    svc.delete_todo(db, todo_id, current_user)
    return None