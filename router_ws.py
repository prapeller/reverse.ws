import time

import fastapi as fa
import psycopg2

from database import SessionLocal
from database.crud import get, remove
from database.models.queue import QueueModel

router = fa.APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[fa.WebSocket] = []

    async def connect(self, websocket: fa.WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: fa.WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: fa.WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def get_last_from_queue():
    session = SessionLocal()
    last_text = None
    queue: QueueModel = get(session, QueueModel)
    if queue is not None:
        last_text = queue.text
        remove(session, QueueModel, id=queue.id)
        session.commit()
    return last_text


@router.websocket("/ws")
async def websocket_endpoint(websocket: fa.WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            text = await get_last_from_queue()
            if text is not None:
                await manager.broadcast(text)
            time.sleep(1)
    except fa.WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{websocket} disconnected")
