from pydantic import BaseModel

from .users import UserSchema


class ClubSchema(BaseModel):
    """Club schema."""

    id: str
    slug: str
    name: str


class MemberSchema(BaseModel):
    """Member schema."""

    user_id: str
    user = UserSchema
    club_id: str
    club: ClubSchema
    active: bool
