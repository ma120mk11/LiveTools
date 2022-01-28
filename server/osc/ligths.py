from osc.osc import OSCBase
import logging

logger = logging.getLogger(__name__)


class OSCLights(OSCBase):

    # TODO Move to db
    cuelists = {
        "frontlights": "/Mx/playback/page5/50/",
        "generic_rock": "/Mx/playback/page1/2/",
        "runaway": "/Mx/playback/page6/0/",
        "speaking": "/Mx/playback/page1/1/",
        "pause": "/Mx/playback/page1/3/",
        "slow_ballad": "/Mx/playback/page3/0/",
        "high_intensity": "/Mx/playback/page3/20/",
        "side_par_red": "/Mx/playback/page1/40/",
        "par_red_blue_fx": "/Mx/playback/page1/25/"
    }
    _active: list = []
    _active_persistent: list = []           # Ex. frontlights that is on the whole set
    _default_cuelist: str = "generic_rock"

    def __init__(self):
        self._name = "Onyx"
        self._type = "Lighting console"
        super().__init__()
        logger.debug("Initializing Onyx")

    def start_cuelist(self, cuelist:list=[], persistent=False):
        for cue in cuelist:
            if not cue in self.cuelists:
                logger.error("Cuelist %s doesn't exist, fallback to default", cue)
                cue = self._default_cuelist

            logger.debug("Cuelist: %s go", cue)

            if persistent:
                self._active_persistent.append(cue)
            else:
                self._active.append(cue)

            self.send_osc_msg(self.cuelists[cue] + "go")
        return

    def release_active_cuelists(self, persistent=False):
        """
        Releases active cuelists. Ignores persistent by default.
        Param:
            persistent=False Set to true to release persistent cuelist also
        """
        logger.debug("Releasing active cuelists")
        if persistent:
            for cue in self._active_persistent:
                self.send_osc_msg(self.cuelists[cue] + "release")
        
        for cue in self._active:
            self.send_osc_msg(self.cuelists[cue] + "release")
        self._active = []

    def get_active(self) -> dict:
        """
        Returns active cuelist, omitting persistent
        """
        return self._active

    def get_active_cuelists(self) -> dict:
        """
        Returns all active cuelist
        """
        return {
            "active": self._active,
            "persistent": self._active_persistent 
        }
