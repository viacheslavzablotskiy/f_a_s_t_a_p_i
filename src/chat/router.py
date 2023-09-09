from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.chat.models import Messages
from src.database import async_session_maker, get_async_session
router = APIRouter(
    prefix='/chat',
    tags=['chat']
)



class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        # if add_bool:
        #     await self.add_message_in_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    # @staticmethod
    # async def add_message_in_database(message: str):
    #     async with async_session_maker() as session:
    #         stmt = insert(Messages).values(text=message)
    #         await session.execute(stmt)
    #         await session.commit()


manager = ConnectionManager()



@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
