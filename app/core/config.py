from pydantic import BaseModel
import os
import secrets


class Settings(BaseModel):
    APP_NAME: str = "FastAPI Todos"
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./todos.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_hex(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()
