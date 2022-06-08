from ipaddress import IPv4Address
import logging
from typing import List
from app.schemas.device import OSCDevice
from app.websocket.connection_manager import manager
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)

class DeviceManager():
    _connected: List[OSCDevice] = []

    def __init__(self) -> None:
        logger.debug("Initializing OSC Device Manager")

    def add_device(self, device_name: str, type: str,) -> int:
        id = len(self._connected)
        logger.debug("Adding device id: %i, name: %s", id, device_name)
        device = OSCDevice(
            name=device_name, 
            type=type, ip = "", 
            receive_port= -1, 
            state="disconnected",
            enabled=True,
            id=len(self._connected))

        self._connected.append(device)

        return id

    def get_ip(self, id: int):
        return self._connected[id].ip

    async def set_ip(self, device_id: int, ip: str):
        self._connected[device_id].ip = ip
        await self.notify_change()
        return self._connected[device_id]

    async def set_receive_port(self, device_id: int, port: int):
        self._connected[device_id].receive_port = port
        await self.notify_change()
        return self._connected[device_id]

    def get_port(self, id:int):
        return self._connected[id].receive_port

    async def set_status(self, device_id: int, status: str):
        if device_id >= 0:
            self._connected[device_id].state = status
        await self.notify_change()

    async def set_enabled(self, device_id: int, status: bool):
        logger.debug("Setting device enabled status")
        if device_id >= 0:
            self._connected[device_id].enabled = status
        await self.notify_change()


    def get_status(self, device_id: int):
        return self._connected[device_id].state

    def get_status(self):
        
        return self._connected
    
    def get_name(self, device_id: int) ->str:
        return self._connected[device_id].name

    async def connect(self, id:int, ip: IPv4Address, port:int):

        self._connected[id].ip = ip
        self._connected[id].receive_port = port
        self._connected[id].state = ""
        await self.notify_change()
        return len(self._connected)


    async def notify_change(self):
        """
        Broadcast all device states
        """
        logger.debug("Notifying change")
        await manager.broadcast(jsonable_encoder(self._connected), notify_type="device-state")

    def get_connected(self) -> List[OSCDevice]:
        return self._connected

device_mgr: DeviceManager = DeviceManager()