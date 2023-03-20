from pydantic import BaseModel


class RoomSchema(BaseModel):
    """Room mongo schema."""

    id: str | None
    slug: str
    club: str
    receivers: list[str]

    class Config:
        orm_mode = True


class MessageSchema(BaseModel):
    """Message mongo schema."""

    id: str | None
    sender: str | None
    room: RoomSchema | None
    text: str | None

    class Config:
        orm_mode = True


class ReadMessageSchema(BaseModel):
    """Read Message mongo schema."""

    id: str | None
    sender: str | None
    text: str | None

    class Config:
        orm_mode = True


class CreateMessageSchema(BaseModel):
    """Create Message mongo schema."""

    text: str | None

    class Config:
        orm_mode = True
