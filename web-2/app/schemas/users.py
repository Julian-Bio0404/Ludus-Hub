from pydantic import BaseModel


class UserSchema(BaseModel):
    """User schema."""

    id: str
    username: str
