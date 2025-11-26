from datetime import datetime, timedelta
from typing import Optional, Tuple, Sequence
import hmac, hashlib, base64, json
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.todo.models import User, UserCreate, Todo, TodoCreate, TodoUpdate
from app.core.config import settings

def _hash_password(password: str) -> str:
    # Simple SHA-256 + secret as salt (use passlib/bcrypt in prod)
    return hashlib.sha256((settings.SECRET_KEY + password).encode()).hexdigest()

def create_user(db: Session, payload: UserCreate) -> User:
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(username=payload.username,
                hashed_password=_hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

def get_user(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user(db, username)
    if not user: return None
    return user if hmac.compare_digest(user.hashed_password, _hash_password(password)) else None

# --- Minimal JWT-like helpers (HS256) ---
def _urlsafe_b64encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

def _urlsafe_b64decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def _sign(data: bytes, secret: str) -> str:
    return _urlsafe_b64encode(hmac.new(secret.encode(), data, hashlib.sha256).digest())

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    exp = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload["exp"] = int(exp.timestamp())
    h_b64 = _urlsafe_b64encode(json.dumps(header, separators=(",", ":")).encode())
    p_b64 = _urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode())
    sig = _sign(f"{h_b64}.{p_b64}".encode(), settings.SECRET_KEY)
    return f"{h_b64}.{p_b64}.{sig}"

def verify_access_token(token: str) -> Tuple[dict, bool]:
    try:
        h_b64, p_b64, sig = token.split(".")
        expected = _sign(f"{h_b64}.{p_b64}".encode(), settings.SECRET_KEY)
        if not hmac.compare_digest(sig, expected): return {}, False
        payload = json.loads(_urlsafe_b64decode(p_b64))
        if "exp" not in payload or datetime.utcnow().timestamp() > payload["exp"]:
            return {}, False
        return payload, True
    except Exception:
        return {}, False


def create_todo(db: Session, payload: TodoCreate, owner: User) -> Todo:
    # Avoid duplicate titles per user (case-insensitive)
    exists = (
        db.query(Todo)
        .filter(Todo.user_id == owner.id, Todo.title.ilike(payload.title))
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Todo with this title already exists")
    todo = Todo(title=payload.title, description=payload.description, user_id=owner.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def list_todos(db: Session, owner: User, skip: int = 0, limit: int = 50) -> Sequence[Todo]:
    return (
        db.query(Todo)
        .filter(Todo.user_id == owner.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_todo(db: Session, todo_id: int, owner: User) -> Todo:
    obj = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == owner.id)
        .first()
    )
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return obj

def update_todo(db: Session, todo_id: int, payload: TodoUpdate, owner: User) -> Todo:
    obj = get_todo(db, todo_id, owner)
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_todo(db: Session, todo_id: int, owner: User) -> None:
    obj = get_todo(db, todo_id, owner)
    db.delete(obj)
    db.commit()