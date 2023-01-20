import time

import fastapi as fa
import sqlalchemy as sa

from database import SessionLocal
from database.models.text import TextModel
from services.ws_manager import manager

router = fa.APIRouter()


def get_last_from_queue():
    text = None
    session = SessionLocal()
    last_text: TextModel = session.query(TextModel) \
        .order_by(sa.desc(TextModel.id)) \
        .limit(1) \
        .first()
    if last_text is not None:
        text = last_text.text
        session.delete(last_text)
        session.commit()
    session.close()
    return text


@router.websocket("/ws")
async def websocket_endpoint(websocket: fa.WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            text = get_last_from_queue()
            if text is not None:
                await manager.broadcast(text)
            time.sleep(1)
    except fa.WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{websocket} disconnected")
