from settings import Base
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from .users import User


class Club(Base):
    """Club model."""

    __tablename__ = 'sports_club'

    id = Column(String, primary_key=True, index=True)
    slug = Column(String, unique=True)
    name = Column(String)
    members = relationship('Member', back_populates='club')


class Member(Base):
    """Member model."""

    __tablename__ = 'sports_member'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users_user.id'))
    user = relationship(User, back_populates='members')
    club_id = Column(String, ForeignKey('sports_club.id'))
    club = relationship('Club', back_populates='members')
    active = Column(Boolean)
