from fastapi import WebSocket, APIRouter

router = APIRouter(
    tags=["Chat"],
)



@router.websocket("/chat/{chat_id}/ws")
async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    """
    WebSocket endpoint for chat
    """
    await websocket.accept()
    await websocket.send_text("Hello World in chat " + chat_id)
    await websocket.receive_json()
