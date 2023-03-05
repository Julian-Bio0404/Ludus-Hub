from mongoengine import Document, ListField, ReferenceField, StringField

from .users import User


class Room(Document):
    """Room mongo model."""

    slug = StringField(required=True, unique=True)
    club = StringField(required=True)
    receivers = ListField(ReferenceField(User))


class Message(Document):
    """Message mongo model."""

    sender = ReferenceField(User, required=True)
    room = ReferenceField(Room, required=True)
    text = StringField(required=True)
