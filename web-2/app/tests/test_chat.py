import pytest
from starlette.testclient import TestClient
# from starlette.websockets import WebSocketDisconnect
from main import app


client = TestClient(app)


class TestClubChatCase:

    def setup_function():
        pass

    def test_ws_user_not_authenticated():
        pass

    def test_ws_club_not_exist():
        pass

    def test_ws_user_not_member():
        pass

    @pytest.mark.asyncio
    async def test_ws_successful_connection():
        pass
