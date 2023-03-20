from pydantic import BaseModel


class RoomSchema(BaseModel):
    """Room mongo model."""

    id: str | None
    slug: str
    club: str
    receivers: list[str]

    class Config:
        orm_mode = True


class MessageSchema(BaseModel):
    """Message mongo model."""

    id: str | None
    sender: str | None
    room: RoomSchema | None
    text: str | None

    class Config:
        orm_mode = True
