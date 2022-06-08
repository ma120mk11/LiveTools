import logging
from typing import Union
from pythonosc import udp_client
from ipaddress import IPv4Address
from app.device_manager import device_mgr

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

    _enabled = True
    _type: str = "undefined"
    _name: str = "undefined"
    _status: str = "disconnected"
    _device_id: int = 100

    _max_retries = 3

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


    def send_osc_msg(self, osc_address: str, value: Union[float, str] = 1, retry_count: int = 0, retry: bool = True):
        """
        Sends a message to the osc device. Value is optional.
        """
        if not osc_address.startswith("/"):
            logger.warning("Osc message doesn't start with /")
            
        self.client = udp_client.SimpleUDPClient(self.get_ip(), self.get_port())
        logger.debug("SEND %s:%i - %s  VALUE: %s", self.client._address, self.client._port, osc_address, value)
        try:
            self.client.send_message(osc_address, value)
        except:
            logger.error("Error sending OSC msg to %s %s:%i - %s  VALUE: %s", self._name, self.client._address, self.client._port, osc_address, value)
            #Retry
            if retry and retry_count <= self._max_retries:
                self.send_osc_msg(osc_address, value, retry_count=retry_count +1)



