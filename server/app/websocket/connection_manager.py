from enum import Enum
import json
import logging
from fastapi import WebSocket
from typing import List, Union

logger = logging.getLogger(__name__)

class MsgType(str, Enum):
    ERROR = "error"
    NOTIFICATION = "notification"
    DEVICE_STATUS = "device-status-change"


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Websocket client connected: %s", client_id)
        await self.broadcast(f"{client_id} connected", "notification")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, receiver: WebSocket ,data: Union[str, dict], notify_type: str = "notification"):
        data = self._format_for_ws(data, notify_type)
        await receiver.send_text(data)

    async def broadcast(self, data: Union[str, dict], notify_type: str = "notification"):
        """
        Broadcasts the message to all connected clients.
        """
        data = self._format_for_ws(data, notify_type)

        for connection in self.active_connections:
            await connection.send_text(data)
    

    @staticmethod
    def _format_for_ws(data: Union[str, dict], notify_type: str):
        if type(data) == "dict":
            data = json.dump(data)
        if type(data) == "str":
            data = f'"{data}"'
        data = json.dumps({"msg_type": notify_type, "data": data})
        return data

manager = ConnectionManager()
