from settings import Base
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class User(Base):
    """User model."""

    __tablename__ = 'users_user'

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True)
    members = relationship('Member', back_populates='user')


class Token(Base):
    """Token model."""

    __tablename__ = 'authtoken_token'

    id = Column(String, primary_key=True, index=True)
    key = Column(String, primary_key=True, unique=True)
    user_id = Column(String, ForeignKey('users_user.id'))
    user = relationship('User', back_populates='token')
    created = Column(DateTime, nullable=False)
