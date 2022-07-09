from app import crud
from app.osc.osc import OSCBase
import logging

from sqlalchemy.orm import Session

from app.schemas.light_cmd import LightCommandShort

logger = logging.getLogger(__name__)


class OSCLights(OSCBase):
    # TODO Move to db
    cuelists = {
        "generic_rock": "/Mx/playback/page5/1/",
        "frontlights": "/Mx/playback/page5/50/",
        "speaking": "/Mx/playback/page5/60/",
        "blackout": "/Mx/playback/page5/70/",
        "pause": "/Mx/playback/page1/3/",
    }
    _active: list = []
    _active_persistent: list = []           # Ex. frontlights that is on the whole set
    _default_cuelist: str = "generic_rock"
    _is_blackout: bool = False

    def __init__(self):
        self._name = "Onyx"
        self._type = "Lighting console"
        super().__init__()
        logger.debug("Initializing Onyx")

    def blackout(self, db: Session, toggle=False):
        if not self._is_blackout:
            self.start_cuelist(db=db, cuelist=['blackout'])
            self._is_blackout = True
        elif toggle and self._is_blackout:
            self.release_cuelist('blackout')
            self._is_blackout = False
        
    def start_cuelist(self, db: Session, cuelist:list=[], persistent=False):
        for cue in cuelist:
            if not isinstance(cue, str) and cue['id']:
                db_cue = crud.light_cmd.get(db=db, id=cue['id'])

                if db_cue:
                    cue = db_cue
                    logger.info(f"Starting cuelist {db_cue.name}")

                    if persistent:
                        # Avoid duplicates
                        if not cue in self._active_persistent:
                            self._active_persistent.append(cue)
                    else:
                        self._active.append(cue)

                    self.send_osc_msg(cue.osc_path + "go")

                else:
                    logger.error(f"Cue with id {cue} not found in database")
                    logger.error(f"Default cue not yet supported")


            else:
                # String name, will be depricated
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

    def release_cuelist(self, cue) -> None:
        """
        Releases a specified cuelist
        """
        if cue in self._active_persistent:
            if isinstance(cue, str):
                logger.debug(f"Releasing cuelist {cue}")
                self.send_osc_msg(self.cuelists[cue] + "release")
                self._active_persistent.remove(cue)
            else:
                logger.debug(f"Releasing cuelist {cue.osc_path}")
                self.send_osc_msg(cue.osc_path + "release")
                self._active_persistent.remove(cue)

        if cue in self._active:
            if isinstance(cue, str):
                logger.debug(f"Releasing cuelist {cue}")
                self.send_osc_msg(self.cuelists[cue] + "release")
                self._active.remove(cue)
            else:
                logger.debug(f"Releasing cuelist {cue.osc_path}")
                self.send_osc_msg(cue.osc_path + "release")
                self._active.remove(cue)



    def release_active_cuelists(self, persistent=False):
        """
        Releases active cuelists. Ignores persistent by default.
        Param:
            persistent=False Set to true to release persistent cuelist also
        """
        logger.debug("Releasing active cuelists")
        if persistent:
            for cue in self._active_persistent:
                if isinstance(cue, str):
                    self.send_osc_msg(self.cuelists[cue] + "release")
                else:
                    self.send_osc_msg(cue.osc_path + "release")
        
        for cue in self._active:
            if isinstance(cue, str):
                self.send_osc_msg(self.cuelists[cue] + "release")
            else:
                self.send_osc_msg(cue.osc_path + "release")

        # TODO: Might need to check logic for blackout
        self._is_blackout = False
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