from osc.ardour_osc import ArdourOSC

import logging

logger = logging.getLogger(__name__)

class OSCRecoding(ArdourOSC):
    # Statuses
    _STOPPED = "stopped"
    _RECORDING = "recording..."

    # Osc commands
    _toggle_record_enable = "/rec_enable_toggle"
    _add_marker = "/add_marker"
    _arm_all_tracks = "/access_action/accessRecorder/arm-all"

    def __init__(self):
        self._type = "multitracking"
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

        return True


    async def stop_recording(self) -> bool:
        logger.debug("Stopping recording")
        self.status = self._STOPPED
        self.send_osc_msg(self._stop)
        self.send_osc_msg(self._toggle_record_enable)

        return True
