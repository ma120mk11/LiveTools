from osc.osc import OSCBase
import logging

logger = logging.getLogger(__name__)


class OSCLights(OSCBase):

    # TODO Move to db
    cuelists = {
        "BACK_PAR_RED": "/Mx/playback/page1/0/",
        "BACK_PAR_GREEN": "/Mx/playback/page1/1/",
        "BACK_PAR_BLUE": "/Mx/playback/page1/2/",
        "BACK_PAR_AMBER": "/Mx/playback/page1/3/",
        "BACK_PAR_YELLOW": "/Mx/playback/page1/4/",
        "BACK_PAR_MAGENTA": "/Mx/playback/page1/5/",

        "BACK_PAR_100": "/Mx/playback/page1/8/",
        "BACK_PAR_0": "/Mx/playback/page1/8/",

        "BACK_PAR_MINT": "/Mx/playback/page1/10/",
        "BACK_PAR_ORANGE": "/Mx/playback/page1/11/",
        "BACK_PAR_PURPLE": "/Mx/playback/page1/12/",
        "BACK_PAR_PINK": "/Mx/playback/page1/13/",
        "BACK_PAR_CYAN": "/Mx/playback/page1/14/",
        "BACK_PAR_R_B_FX": "/Mx/playback/page1/15/",

        "frontlights": "/Mx/playback/page5/50/",
        "generic_rock": "/Mx/playback/page5/1/",
        "red_ambient": "/Mx/playback/page5/6/",
        "blue_amber": "/Mx/playback/page5/10/",
        "green_rocker": "/Mx/playback/page5/20/",

        "runaway": "/Mx/playback/page6/0/",
        "bourbon_street": "/Mx/playback/page6/1/",
        "born_to_run": "/Mx/playback/page6/2/",
        "flickorna_tv2": "/Mx/playback/page6/3/",
        "rosanna": "/Mx/playback/page6/4/",
        "boys_of_summer": "/Mx/playback/page6/5/",
        "when_youre_gone": "/Mx/playback/page6/6/",
        "died_in_your_arms": "/Mx/playback/page6/7/",

        "heavy_red": "/Mx/playback/page5/0/",
        "speaking": "/Mx/playback/page1/1/",
        "pause": "/Mx/playback/page1/3/",
        "slow_ballad": "/Mx/playback/page5/2/",
        "high_intensity": "/Mx/playback/page3/20/",
        "side_par_red": "/Mx/playback/page1/40/",
        "par_red_blue_fx": "/Mx/playback/page1/25/",
        "in_time_youll_find_v1": "/Mx/playback/page10/1/"
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
                # Avoid duplicates
                if not cue in self._active_persistent:
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
    def get_cuelist(self) -> dict:
        """
        Returns all available cuelists
        """
        return self.cuelists