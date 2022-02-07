import asyncio
from ipaddress import IPv4Address
import logging
from .osc import OSCBase
from .osc_server import server

logger = logging.getLogger(__name__)

class ArdourOSC(OSCBase):
    """
    Ardour specific OSC
        Implements Ardour OSC Heartbeat
    """

    _set_surface = "/set_surface"   # Enables OSC heartbeat in Ardour
    _play = "/transport_play"
    _stop = "/transport_stop"

    def __init__(self):
        super().__init__()

    def _init_heartbeat(self):
        self.send_osc_msg(self._set_surface, 8)

    async def connect(self, ip: IPv4Address, port: int):
        await super().connect(ip, port)
        server.add_heartbeat("/heartbeat", 3, self.connection_change_handler, self._device_id)
        self._init_heartbeat()

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
        Automaticly try to re-connect
        """
        while self.status != self._CONNECTED or self._enabled:
            self._init_heartbeat()
            await asyncio.sleep(5)

    async def test_connection(self) -> bool:
        """
        Ardour uses a heartbeat instead of test
        """
        return True