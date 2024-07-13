import uuid

from pydantic import BaseModel

from .users import UserSchema


class ClubSchema(BaseModel):
    """Club schema."""

    id: uuid.UUID
    slug: str
    name: str

    class Config:
        from_attributes = True


class MemberSchema(BaseModel):
    """Member schema."""

    user_id: uuid.UUID
    user = UserSchema
    club_id: uuid.UUID
    club: ClubSchema
    active: bool

    class Config:
        from_attributes = True
