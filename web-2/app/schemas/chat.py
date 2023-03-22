from pydantic import BaseModel, Field


class ReadMessageSchema(BaseModel):
    """Read Message mongo schema."""

    id: str = Field(alias='_id')
    sender: str | None
    text: str | None
    date: str
    room: str

    class Config:
        orm_mode = True
