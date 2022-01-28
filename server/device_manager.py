from ipaddress import IPv4Address
import logging
from os import name
from typing import List, Union
from fastapi import status
from schemas import DeviceState, OSCDevice
from websocket.connection_manager import manager
from fastapi.encoders import jsonable_encoder

# x_air: OSCDevice = OSCDevice(
#     id=1,
#     name="XAIR-18",
#     ip="192.168.43.20",
#     send_port=7300,
#     receive_port=7301,
#     state="connected"
# )


logger = logging.getLogger(__name__)

class DeviceManager():
    _connected: List[OSCDevice] = []

    def __init__(self) -> None:
        logger.debug("Initializing OSC Device Manager")
        # self._connected.append(x_air)

    def add_device(self, device_name: str, type: str,) -> int:
        id = len(self._connected)
        logger.debug("Adding device id: %i, name: %s", id, device_name)
        device = OSCDevice(
            name=device_name, 
            type=type, ip = "", 
            receive_port= -1, 
            state="disconnected",
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

    def set_status(self, device_id: int, status: str):
        pass
        # if device_id >= 0:
            # self._connected[device_id].state = status            

    def get_status(self, device_id: int):
        return self._connected[device_id].state

    def get_status(self):
        
        return self._connected
    

    async def connect(self, id:int, ip: IPv4Address, port:int):

        self._connected[id].ip = ip
        self._connected[id].receive_port = port
        self._connected[id].state = "connected"
        await self.notify_change()
        return len(self._connected)

    # def edit_connection(self, device_id: int, ip: IPv4Address, port: int):
    #     self._connected[device_id].ip = ip
    #     self._connected[device_id].receive_port = port
    #     return self.

    async def notify_change(self):
        """
        Broadcast all device states
        """
        logger.debug("Notifying change")
        await manager.broadcast(jsonable_encoder(self._connected), notify_type="device-state")

    def get_connected(self) -> List[OSCDevice]:
        return self._connected

device_mgr: DeviceManager = DeviceManager()