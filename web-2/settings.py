"""Web 2 settings."""

import logging
from functools import lru_cache
from pathlib import Path

from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .main import app


# ------------ SETTINGS CONFIGURATIONS ------------ #
class Settings(BaseSettings):
    """FastApi settings."""

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    test_postgres_db: str
    test_postgres_user: str
    test_postgres_password: str
    test_postgres_host: str
    test_postgres_port: str

    mongo_initdb_root_username: str
    mongo_initdb_root_password: str

    class Config:
        env_file = str(Path(__file__).parent.parent / ".env")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

# ------------ DATABASE CONFIGURATION ------------ #
DATABASE_URL = f'postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}'  # NOQA
MONGODB_URL = f'mongodb://{settings.mongo_initdb_root_username}:{settings.mongo_initdb_root_password}@mongodb:27017'

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


# ------------ TESTING DATABASE CONFIGURATION ------------ #
TEST_DATABASE_URL = f'postgresql://{settings.test_postgres_user}:{settings.test_postgres_password}@{settings.test_postgres_host}/{settings.test_postgres_db}'  # NOQA

test_postgres_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_postgres_engine)
Base.metadata.create_all(bind=test_postgres_engine)


def override_get_db():
    """Get testing session of postgres db."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ------------ LOGGER CONFIGURATION ------------ #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
