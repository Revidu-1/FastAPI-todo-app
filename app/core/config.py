from pydantic import BaseModel
import os

class Settings(BaseModel):
    APP_NAME: str = "FastAPI Todos"
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./todos.db")

settings = Settings()
