import asyncio
import socket
import argparse
import random
import time
import math
import threading
import logging
from typing import Callable, List, Union
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from ipaddress import IPv4Address
from schemas import OSCDevice
from device_manager import device_mgr
from pydantic import BaseModel
from time import monotonic as time, sleep

logger = logging.getLogger(__name__)

class OSCBase():
    # Device network setup
    client_ip: IPv4Address
    client_port: int
    client: udp_client.SimpleUDPClient = None
    
    # Statuses
    _CONNECTED = "connected"
    _NOT_CONNECTED = "not_connected"
    _NO_HEARTBEAT = "no_heartbeat"
    _CONNECTION_NOT_KNOWN = "connection_not_known"
    _DISABLED = "disabled"
    _READY = "ready"
    _INITIALIZED = "initialized"

    _type: str = "undefined"
    _name: str = "undefined"
    _status: str = "disconnected"
    _device_id: int = 100

    def __init__(self):
        self._device_id = device_mgr.add_device(self._name, self._type)

    @property
    def status(self):
        return self._status

    @status.setter
    async def status(self, new_status):
        self._status = new_status
        await device_mgr.set_status(self._device_id, self.status)
        return self._status

    async def set_status(self, new_status):
        self._status = new_status
        await device_mgr.set_status(self._device_id, self.status)
        return self._status

    

    async def connect(self, ip: IPv4Address, port: int) -> bool:
        logger.debug("Connecting %s to %s:%i", __name__, ip, port)
        self.client_ip = ip
        self.client_port = port
        await device_mgr.connect(self._device_id, self.client_ip,self.client_port)
        return 1


    def get_ip(self):
        """
        Returns the ip for the OSC device
        """
        return device_mgr.get_ip(self._device_id)

    def get_name(self):
        """
        Returns the name of the device
        """
        return device_mgr.get_name(self._device_id)

    def get_port(self):
        """
        Returns the configured port for the device
        """
        return device_mgr.get_port(self._device_id)


    def test_connection(self) -> bool:
        """
        Method should be implemented by classes inheriting osc.
        Should send an osc message and listen for feedback.
        """
        logger.debug("Testing OSC connection for: %s", self.get_name())


    def send_osc_msg(self, osc_address: str, value: Union[float, str] =1 ):
        """
        Sends a message to the osc device. Value is optional.
        """

        self.client = udp_client.SimpleUDPClient(self.get_ip(), self.get_port())
        logger.debug("SEND %s:%i - %s  VALUE: %s", self.client._address, self.client._port, osc_address, value)
        try:
            self.client.send_message(osc_address, value)
        except:
            logger.error("Error sending OSC message: %s:%i - %s  VALUE: %s", self.client._address, self.client._port, osc_address, value)




class Heartbeat(BaseModel):
    last_heartbeat: float
    route: str
    is_connected: bool
    device_mgr_id: int
    timeout: int
    error_callback: Callable



class OSCServer:

    server_ip: IPv4Address = "192.168.43.249"
    server_port = 8000
    server: osc_server.ThreadingOSCUDPServer = None
    dispatch: dispatcher.Dispatcher = None
    _status: str = ""

    _heartbeats: List[Heartbeat] = []
    _heartbeat_thread = None

    def getServerIP(self) -> IPv4Address:
        hostname = socket.gethostname()
        server_ip: IPv4Address = IPv4Address(socket.gethostbyname(hostname))
        return server_ip

    def stop_osc_server(self):
        logger.debug("Shutting down osc server...")
        self.server.shutdown()
        return



    def start_osc_server(self) -> bool:

        if not self.server_ip:
            self.server_ip = self.getServerIP()

        logger.info("Starting OSC Server...")
        self.dispatch = dispatcher.Dispatcher()

        # self.addMap("/1/toggle1")

        try:
            self.server = osc_server.ThreadingOSCUDPServer(
                (self.server_ip, self.server_port), self.dispatch)

            logger.info("Serving on {}".format(self.server.server_address))

            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.start()

            # self._heartbeat_thread = threading.Thread(target=self.heartbeat_check)
            asyncio.create_task(self.heartbeat_check())
            # self._heartbeat_thread.start()
            return 1
        except Exception as e:
            logger.error("Error starting OSC server: ")
            return 0


    def addMap(self, route:str):
        logger.debug("Adding map '%s' to dispatcher...", route)
        if self.dispatch is None:
            logger.error("dispatcher not initialized")
        else:
            self.dispatch.map(route, print)

    def add_map(self, route:str, callback, id):
        logger.debug("Adding map '%s' to dispatcher...", route)
        if self.dispatch is None:
            logger.error("dispatcher not initialized")
        else:
            self.dispatch.map(route, callback, id, needs_reply_address=True)


    async def heartbeat_check(self):
        logger.debug("heartbeat function started")
        while True:
            current_time = time()
            for device in self._heartbeats:
                if current_time - device.last_heartbeat > device.timeout:
                    if device.is_connected:
                        await device.error_callback(connected=False)
                        device.is_connected = False
                else:
                    if not device.is_connected:
                        await device.error_callback(connected=True)
                        device.is_connected = True

            await asyncio.sleep(1)


    def add_heartbeat(self, route: str, timeout: int, callback: Callable, device_id):
        logger.debug("Adding heartbeat to listener")
        heartbeat: Heartbeat = Heartbeat(
            last_heartbeat=time(),
            route=route,
            device_mgr_id = device_id,
            is_connected=False,
            timeout=timeout,
            error_callback=callback
        )        
        self._heartbeats.append(heartbeat)
        id = len(self._heartbeats) -1
        self.add_map(route, self.set_last_time, id)


    def set_last_time(self, *args, **kwargs):
        sender_ip_address: str = args[0][0]
        id: int = args[2][0]

        if sender_ip_address == device_mgr.get_ip(self._heartbeats[id].device_mgr_id):
            self._heartbeats[id].last_heartbeat=time()


server = OSCServer()