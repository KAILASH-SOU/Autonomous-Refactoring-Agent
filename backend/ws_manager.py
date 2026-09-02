from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_log(self, message: str, level: str = "info"):
        for connection in self.active_connections:
            await connection.send_json({
                "type": "log",
                "payload": {
                    "level": level,
                    "message": message
                }
            })

    async def send_diff(self, original: str, modified: str):
        for connection in self.active_connections:
            await connection.send_json({
                "type": "diff",
                "payload": {
                    "original": original,
                    "modified": modified
                }
            })

manager = ConnectionManager()
