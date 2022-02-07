import asyncio
from ipaddress import IPv4Address
import logging
import socket
import threading
from typing import Callable, List
from device_manager import device_mgr
from pythonosc import osc_server, dispatcher
from time import monotonic as time
from pydantic import BaseModel


class Heartbeat(BaseModel):
    last_heartbeat: float
    route: str
    is_connected: bool
    device_mgr_id: int
    timeout: int
    on_status_change_callback: Callable

logger = logging.getLogger(__name__)


class OSCServer:

    server_ip: IPv4Address = "192.168.43.249"
    server_port = 8000
    server: osc_server.ThreadingOSCUDPServer = None
    dispatch: dispatcher.Dispatcher = None
    _status: str = ""

    _heartbeats: List[Heartbeat] = []
    _heartbeat_thread = None

    def get_server_ip(self) -> IPv4Address:
        hostname = socket.gethostname()
        server_ip: IPv4Address = IPv4Address(socket.gethostbyname(hostname))
        return server_ip

    def stop_osc_server(self):
        logger.debug("Shutting down osc server...")
        self.server.shutdown()
        return



    def start_osc_server(self) -> bool:

        if not self.server_ip:
            self.server_ip = self.get_server_ip()

        logger.info("Starting OSC Server...")
        self.dispatch = dispatcher.Dispatcher()

        # self.addMap("/1/toggle1")

        try:
            self.server = osc_server.ThreadingOSCUDPServer(
                (self.server_ip, self.server_port), self.dispatch)

            logger.info("Serving on {}".format(self.server.server_address))

            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.start()

            asyncio.create_task(self.heartbeat_listener())

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

    def add_map(self, route:str, callback: Callable, id: int):
        """
        Adds a map with a callback function to the Dispatcher.
        """

        logger.debug("Adding map '%s' to dispatcher...", route)
        if self.dispatch is None:
            logger.error("dispatcher not initialized")
        else:
            self.dispatch.map(route, callback, id, needs_reply_address=True)


    async def heartbeat_listener(self):
        """
        Listens to heartbeats and executes the heartbeat callback
        function on connection change.
        """
        logger.debug("Heartbeat listener started")

        while True:
            for device in self._heartbeats:
                current_time = time()
                if current_time - device.last_heartbeat > device.timeout:
                    if device.is_connected:
                        await device.on_status_change_callback(connected=False)
                        device.is_connected = False
                else:
                    if not device.is_connected:
                        await device.on_status_change_callback(connected=True)
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
            on_status_change_callback=callback
        )        
        self._heartbeats.append(heartbeat)
        id = len(self._heartbeats) -1
        self.add_map(route, self._on_heartbeat_received, id)


    def _on_heartbeat_received(self, *args, **kwargs):
        """
        Callback function for a received heartbeat
        """
        sender_ip_address: str = args[0][0]
        id: int = args[2][0]

        if sender_ip_address == device_mgr.get_ip(self._heartbeats[id].device_mgr_id):
            self._heartbeats[id].last_heartbeat=time()


server = OSCServer()