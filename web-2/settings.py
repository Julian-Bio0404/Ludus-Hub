"""Web 2 settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    """FastApi settings."""

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    mongo_initdb_root_username: str
    mongo_initdb_root_password: str

    class Config:
        env_file = str(Path(__file__).parent.parent / ".env")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

DATABASE_URL = f'postgresql://{settings.postgres_user}:{settings.postgres_password}\
@{settings.postgres_host}/{settings.postgres_db}'

MONGODB_URL = f'mongodb://{settings.mongo_initdb_root_username}:\
{settings.mongo_initdb_root_password}@mongodb:27017'

postgres_engine = create_engine(DATABASE_URL)
mongo_client = MongoClient(MONGODB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)

Base = declarative_base()


def get_db():
    """Get session of postgres db."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
