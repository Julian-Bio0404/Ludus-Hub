"""Web 2 settings."""

from functools import lru_cache

from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path


class Settings(BaseSettings):
    """FastApi settings."""

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    class Config:
        env_file = str(Path(__file__).parent.parent / ".env")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

DATABASE_URL = f'postgresql://{settings.postgres_user}:{settings.postgres_password}\
@{settings.postgres_host}/{settings.postgres_db}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
