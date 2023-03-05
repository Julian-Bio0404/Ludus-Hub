from app.queries import clubs
from app.schemas.clubs import ClubSchema
from fastapi import Depends, FastAPI, HTTPException
from settings import get_db
from sqlalchemy.orm import Session

app = FastAPI()


@app.get('/main')
def main():
    return 'Hello World'


@app.get('/club/{slug}', response_model=ClubSchema)
def read_club(slug: str, db: Session = Depends(get_db)):
    club = clubs.get_club(db, slug=slug)
    if not club:
        raise HTTPException(status_code=404, detail='Club does not exists')
    return club
