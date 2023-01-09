# import pytest

# # Channels
# from channels.testing import WebsocketCommunicator

# # Consumers
# from apps.chat.consumers import ChatConsumer

# # Factories
# from .factories import get_club_factory, get_room, get_token, get_user_factory

# pytestmark = pytest.mark.django_db


# class TestChatCase:

#     @pytest.mark.asyncio
#     async def test_connect(self):
#         user = await get_user_factory()
#         key = await get_token(user)
#         club = await get_club_factory(trainer=user)
#         room = await get_room(club)
#         path = f'/ws/chat/{room}/?token={key}'
#         communicator = WebsocketCommunicator(application=ChatConsumer.as_asgi(), path=path)
#         connected, _ = await communicator.connect()
#         assert not connected
