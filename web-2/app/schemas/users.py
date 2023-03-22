import uuid

from pydantic import BaseModel


class UserSchema(BaseModel):
    """User schema."""

    id: uuid.UUID
    username: str
