import asyncio
from ipaddress import IPv4Address
from .osc import OSCBase, server
from device_manager import device_mgr

import logging

logger = logging.getLogger(__name__)

class OSCRecoding(OSCBase):
    # Statuses
    _STOPPED = "stopped"
    _RECORDING = "recording..."

    # Osc commands
    # _test = "/strip/list"           #Command for testing connection
    _set_surface = "/set_surface"           #Command for testing connection
    _play = "/transport_play"
    _stop = "/transport_stop"
    _toggle_record_enable = "/rec_enable_toggle"
    _add_marker = "/add_marker"
    _arm_all_tracks = "/access_action/accessRecorder/arm-all"

    def __init__(self):
        self._type = "multitacking"
        self._name = "Ardour recording"
        super().__init__()
        logger.debug("Initializing recording")
    
    def _init_heartbeat(self):
        self.send_osc_msg(self._set_surface, 8)
        
    async def connect(self, ip: IPv4Address, port: int):
        await super().connect(ip, port)
        server.add_heartbeat("/heartbeat", 3, self.connection_change_handler, self._device_id)
        self._init_heartbeat()

    async def connection_change_callback(self, ):
        pass


    def create_marker(self):
        logger.debug("Creating marker in Ardour")
        self.send_osc_msg(self._add_marker)

    async def record(self) -> bool:
        logger.debug("Starting recording via OSC")
        self.send_osc_msg(self._toggle_record_enable)
        self.send_osc_msg(self._play)

        # coro = 
        # await self.status(self._RECORDING)
        # self.status = self._RECORDING
        return True

    async def stop_recording(self) -> bool:
        logger.debug("Stopping recording")
        self.status = self._STOPPED
        self.send_osc_msg(self._stop)
        self.send_osc_msg(self._toggle_record_enable)

        return True

    async def test_connection(self) -> bool:
        super().test_connection()
        self.send_osc_msg(self._set_surface)

        return True

    async def connection_change_handler(self, *args, **kwargs):
        """
        Callback method to be called when a connection change is noted.
        ``kwargs: connected: bool``
        """
        if kwargs.get('connected'):
            logger.info("%s re-connected", self._name)
            self._init_heartbeat()
            await self.set_status(self._CONNECTED)
        else:
            logger.error("%s disconnected", self._name)
            await self.set_status(self._NO_HEARTBEAT)
            asyncio.create_task(self._connection_retry())

    async def _connection_retry(self):
        """
        
        """
        while self.status != self._CONNECTED:
            self._init_heartbeat()
            await asyncio.sleep(5)