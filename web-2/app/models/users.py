from settings import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(Base):
    """User model."""

    __tablename__ = 'users_user'

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True)
    members = relationship('Member', back_populates='user')
