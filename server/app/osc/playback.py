import asyncio
from app.osc.ardour_osc import ArdourOSC
import logging

logger = logging.getLogger(__name__)

class OSCPlayback(ArdourOSC):

    #Osc commands
    _save = "/save_state"


    # Current state
    _is_playing: bool = False

    def __init__(self):
        self._type = "playback"
        self._name = "Ardour playback"
        super().__init__()
        logger.debug("Initializing audio playback")

    def start(self, marker: str):
        logger.debug("Starting audio playback from %s", marker)
        self._is_playing = True
        self.send_osc_msg("/marker", marker)
        self.send_osc_msg(self._play)


    async def stop(self, force_send=True):
        if self._is_playing or force_send:
            logger.debug("Stopping Ardour playback")
            self.send_osc_msg(self._stop)

            # TODO: Fix ugly workaround for ardour bug
            await asyncio.sleep(0.1)

            # Go to a safe marker, in case the next marker is not found
            self.goto_safe_marker()
            # self.send_osc_msg(self._save)
            self._is_playing = False

    def goto_safe_marker(self):
        # TODO: Should go to end marker
        self.send_osc_msg("/marker", "safe")
