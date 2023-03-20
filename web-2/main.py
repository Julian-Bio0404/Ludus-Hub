from app.queries import clubs
from app.schemas.chat import MessageSchema
from app.schemas.clubs import ClubSchema
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from settings import get_db, mongo_client
from sqlalchemy.orm import Session

app = FastAPI()


@app.get('/club/{slug}', response_model=ClubSchema)
def read_club(slug: str, db: Session = Depends(get_db)):
    club = clubs.get_club(db, slug=slug)
    if not club:
        raise HTTPException(status_code=404, detail='Club does not exists')
    return club


@app.post('/send-message', response_model=MessageSchema, status_code=201)
def send_message(message: MessageSchema):
    """Send a message."""
    data = jsonable_encoder(message)
    message = mongo_client.local.messages.insert_one(data)
    return message


@app.get('/messages', response_model=list[MessageSchema])
def get_messages():
    """Get all messages."""
    messages = mongo_client.local.messages.find()
    return [MessageSchema(**message) for message in messages]
