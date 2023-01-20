import fastapi as fa


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
