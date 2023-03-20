from mongoengine import Document, ListField, StringField


class Room(Document):
    """Room mongo model."""

    slug = StringField(required=True, unique=True)
    club = StringField(required=True)
    receivers = ListField(StringField(required=True))


class Message(Document):
    """Message mongo model."""

    sender = StringField(required=True)
    room = StringField(required=True)
    text = StringField(required=True)
