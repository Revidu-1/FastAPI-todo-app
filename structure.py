import os, textwrap, pathlib
root = pathlib.Path(".")

# Create packages
pkgs = [
    "app",
    "app/core",
    "app/db",
    "app/models",
    "app/services",
    "app/lib",
    "app/lib/v1",
    "app/lib/v1/endpoints",
]
for p in pkgs:
    (root / p).mkdir(parents=True, exist_ok=True)
    (root / p / "__init__.py").write_text("", encoding="utf-8")

# Files content
files = {
"requirements.txt": """fastapi>=0.112
uvicorn[standard]>=0.29
SQLAlchemy>=2.0
pydantic>=2.7
python-dotenv>=1.0
""",

"app/core/config.py": textwrap.dedent("""
    from pydantic import BaseModel
    import os

    class Settings(BaseModel):
        APP_NAME: str = "FastAPI Todos"
        API_PREFIX: str = "/api"
        API_VERSION: str = "v1"
        SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./todos.db")

    settings = Settings()
"""),

"app/db/base.py": textwrap.dedent("""
    from sqlalchemy.orm import DeclarativeBase
    class Base(DeclarativeBase):
        pass
"""),

"app/db/session.py": textwrap.dedent("""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.core.config import settings

    connect_args = {"check_same_thread": False} if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite") else {}
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args=connect_args)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
"""),

"app/models/todo.py": textwrap.dedent("""
    # SQLAlchemy model + Pydantic schemas in one module (keeps only the requested dirs)
    from sqlalchemy import String, Boolean, Integer
    from sqlalchemy.orm import Mapped, mapped_column
    from pydantic import BaseModel, Field
    from app.db.base import Base

    # ---- SQLAlchemy ORM ----
    class Todo(Base):
        __tablename__ = "todos"
        id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
        title: Mapped[str] = mapped_column(String(200), index=True)
        description: Mapped[str | None] = mapped_column(String(1000), default=None)
        completed: Mapped[bool] = mapped_column(Boolean, default=False)

    # ---- Pydantic Schemas ----
    class TodoBase(BaseModel):
        title: str = Field(..., min_length=1, max_length=200)
        description: str | None = Field(default=None, max_length=1000)

    class TodoCreate(TodoBase):
        pass

    class TodoUpdate(BaseModel):
        title: str | None = Field(default=None, min_length=1, max_length=200)
        description: str | None = Field(default=None, max_length=1000)
        completed: bool | None = None

    class TodoOut(TodoBase):
        id: int
        completed: bool
        model_config = {"from_attributes": True}
"""),

"app/services/todo_service.py": textwrap.dedent("""
    from sqlalchemy.orm import Session
    from fastapi import HTTPException, status
    from typing import Sequence
    from app.models.todo import Todo, TodoCreate, TodoUpdate

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
"""),

"app/lib/deps.py": textwrap.dedent("""
    from typing import Generator
    from app.db.session import SessionLocal

    def get_db() -> Generator:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
"""),

"app/lib/v1/router.py": textwrap.dedent("""
    from fastapi import APIRouter
    from .endpoints import todos

    router_v1 = APIRouter()
    router_v1.include_router(todos.router, prefix="/todos", tags=["todos"])
"""),

"app/lib/v1/endpoints/todos.py": textwrap.dedent("""
    from fastapi import APIRouter, Depends, status
    from sqlalchemy.orm import Session
    from app.lib.deps import get_db
    from app.models.todo import TodoCreate, TodoUpdate, TodoOut
    from app.services import todo_service as svc

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
"""),

"app/main.py": textwrap.dedent("""
    from fastapi import FastAPI
    from app.core.config import settings
    from app.db.session import engine
    from app.db.base import Base
    from app.lib.v1.router import router_v1

    app = FastAPI(title=settings.APP_NAME)

    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    app.include_router(router_v1, prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}")

    @app.get("/health")
    def health():
        return {"status": "ok"}
"""),
}

for path, content in files.items():
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + "\n", encoding="utf-8")

print("✅ Module-based scaffold created (core, db, models, services, lib).")
