import socket
import argparse
import random
import time
import math
import threading
import logging
from typing import Union
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from ipaddress import IPv4Address
from schemas import OSCDevice
from device_manager import device_mgr, DeviceManager

logger = logging.getLogger(__name__)

class OSCBase():
    # Device network setup
    client_ip: IPv4Address
    client_port: int
    client: udp_client.SimpleUDPClient = None
    
    # Statuses
    _NOT_CONNECTED = "not_connected"
    _DISABLED = "disabled"
    _READY = "ready"
    _CONNECTED = "connected"
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


    def get_port(self):
        return device_mgr.get_port(self._device_id)


    def start_osc_client(self):
        logger.info("Starting OSC client...")

        # client = udp_client.SimpleUDPClient(self.client_ip, self.client_port)
        # thread = threading.Thread()
        # thread.start()

    def stop_osc_client(self):
        logger.info("Stopping OSC client...")


    def send_osc_msg(self, osc_address: str, value: Union[float, str] =1 ):
        logger.debug("Send msg to: " + self.get_ip())
        self.client = udp_client.SimpleUDPClient(self.get_ip(), self.get_port())
        logger.debug("SEND %s:%i - %s  VALUE: %s", self.client._address, self.client._port, osc_address, value)
        try:
            self.client.send_message(osc_address, value)
        except:
            logger.error("Error sending OSC message: %s:%i - %s  VALUE: %s", self.client._address, self.client._port, osc_address, value)








class OSCServer:

    server_ip: IPv4Address = "192.168.43.249"
    server_port = 8000
    server: osc_server.ThreadingOSCUDPServer = None
    dispatch: dispatcher.Dispatcher = None
    _status: str = ""


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

            print("Serving on {}".format(self.server.server_address))

            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.start()
            return 1
        except Exception:
            logger.error("Error starting OSC server")
            return 0

    def addMap(self, route:str):
        print("Adding map to dispatcher...")
        if self.dispatch is None:
            print("dispatcher not initialized")
        else:
            self.dispatch.map(route, print)