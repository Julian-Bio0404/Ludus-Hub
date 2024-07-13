# import pytest
# from starlette.testclient import TestClient
# from fastapi import status
# # from starlette.websockets import WebSocketDisconnect
# from main import app


# client = TestClient(app)


# class TestClubChatCase:

#     def setup_function(self):
#         pass

#     def test_ws_user_not_authenticated(self):
#         pass

#     def test_ws_club_not_exist(self):
#         pass

#     @pytest.mark.asyncio
#     def test_ws_user_not_member(self):
#         club_id = "12616266-99c9-4247-bcdc-7871c0c1f878"
#         url = f'/chat/clubs/{club_id}/ws?token=831c57f147de60ce6728b3b45581a91a69753466'
#         try:
#             with client.websocket_connect(url) as websocket:
#                 websocket.
#         except status.WS_1008_POLICY_VIOLATION:
#             assert True

    # @pytest.mark.asyncio
    # async def test_ws_successful_connection(self):
    #     club_id = "12616266-99c9-4247-bcdc-7871c0c1f878"
    #     url = f'/chat/clubs/{club_id}/ws?token=831c57f147de60ce6728b3b45581a91a69753465'
    #     with client.websocket_connect(url) as websocket:
    #         data = websocket.receive_json()
    #         assert data == {"msg": "Hello WebSocket"}
