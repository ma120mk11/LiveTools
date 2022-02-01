from ipaddress import IPv4Address
from .osc import OSCBase
import logging

logger = logging.getLogger(__name__)

class OSCRecoding(OSCBase):
    # Statuses
    _STOPPED = "stopped"
    _RECORDING = "recording..."

    # Osc commands
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

    def create_marker(self):
        logger.debug("Creating marker in Ardour")
        self.send_osc_msg(self._add_marker)

    async def record(self) -> bool:
        logger.debug("Starting recording via OSC")
        self.send_osc_msg(self._toggle_record_enable)
        self.send_osc_msg(self._play)

        # coro = 
        # await self.status(self._RECORDING)
        self.status = self._RECORDING
        return True

    async def stop_recording(self) -> bool:
        logger.debug("Stopping recording")
        self.status = self._STOPPED
        self.send_osc_msg(self._stop)
        self.send_osc_msg(self._toggle_record_enable)

        return True