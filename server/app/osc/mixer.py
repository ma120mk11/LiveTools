from app.osc.x_air import XairOSC
import logging

logger = logging.getLogger(__name__)


class OSCMixer(XairOSC):

    def __init__(self):
        self._name = "X-Air"
        self._type = "Audio console"
        super().__init__()
        logger.debug("Initializing Mixer")