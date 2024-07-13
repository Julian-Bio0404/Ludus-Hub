from sqlalchemy.orm import Session
from typing import Union
from app.models.clubs import Club, Member


def get_club(db: Session, id: str) -> Union[Club, None]:
    return db.query(Club).get(id)


def get_members(db: Session, club_id: str) -> list[Member]:
    members = []
    club = get_club(db, club_id)
    if club:
        members = db.query(Member).filter(Member.club_id == club.id).all()
    return members
