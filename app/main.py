import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.todo import router as todo_router
from app.auth import routes as auth_routes
from app.middleware.request_id_middleware import RequestIDMiddleware
from app.middleware.logging_middleware import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = FastAPI(title=settings.APP_NAME)

# Add CORS middleware (must be before other middlewares)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middlewares (order matters: RequestID before Logging)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router, prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}")
app.include_router(todo_router, prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}/todos", tags=["todos"])

@app.get("/health")
def health():
    return {"status": "ok"}
