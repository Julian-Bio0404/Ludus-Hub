from sqlalchemy.orm import Session
from typing import Union
from app.models.users import User


def get_user(db: Session, id: str) -> Union[User, None]:
    return db.query(User).get(id)
