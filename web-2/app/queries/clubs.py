from sqlalchemy.orm import Session

from app.models.clubs import Club, Member


def get_club(db: Session, slug: str):
    return db.query(Club).filter(Club.slug == slug).first()


def get_members(db: Session, club_slug: str):
    members = None
    club = db.query(Club).filter(Club.slug == club_slug).first()
    if club:
        members = db.query(Member).filter(Member.club_id == club.id).all()
    return members
