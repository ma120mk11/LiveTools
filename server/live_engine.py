import logging
from sqlite3 import connect
from osc.ligths import OSCLights
from osc.playback import OSCPlayback
from websocket.connection_manager import manager, MsgType
from osc.recording import OSCRecoding
# import json
logger = logging.getLogger(__name__)

class Engine():
    _setlist = {}
    _status = "stopped"
    _current_id = -1

    def __init__(self):
        logger.info("Engine initializing")
        self.recording = OSCRecoding()
        self.lights = OSCLights()
        self.playback = OSCPlayback()

    async def start_osc(self):
        logger.info("Connecting all OSC devices...")
        await self.lights.connect("192.168.43.120", 8887)
        await self.recording.connect("192.168.43.120", 3819)
        await self.playback.connect("192.168.43.121", 3819)


    def get_status(self) -> str:
        return self._status

    def get_engine_state(self) -> dict:
        """
        Returns current engine state
            setlist:
            action_id: Current executing action. -1: engine is stopped
            status:
        """

        return {
            "setlist": self._setlist,
            "action_id": self._current_id,
            "status": self._status
        }

    async def load_setlist(self, set: dict):
        """Loads a set"""
        logger.info("Loading setlist: %s", set['name'])
        
        # TODO: How to handle loading a setlist if engine is running
        self._reset_engine()

        self._setlist = set
        await manager.broadcast(self._setlist, "load-set")


    async def start_set(self):
        """Starts the loaded set"""
        # No set loaded
        if not self._setlist:
            logger.error("Unable to start set: No set loaded")
            return 
        if self._current_id >= 0:
            logger.error("Unable to start set: A set is already running")
            return

        self._current_id = 0            # First action
        self._status = "set_running"
        await self.recording.record()

        # Set frontlights and leave them on for rest of the set
        self.lights.start_cuelist(["frontlights"], persistent=True)

        # Automatically start action 0
        await self.next_event("engine")


    async def end_set(self) -> None:
        """
        Ends a running set
        """
        logger.info("Ending set...")

        await manager.broadcast("end-set", "end-set")

        self.lights.release_active_cuelists()
        self.recording.stop_recording()

        self._reset_engine()
        

    async def next_event(self, event_initiator:str = ""):
        logger.info("Next event triggered by %s", event_initiator)

        if self.get_status() != "set_running":
            await manager.broadcast("Set is not started", "notification-warning")
            logger.info("Set is not started")
            return
        
        if self._current_id >= len(self._setlist['actions']):
            await self.end_set()
            return
        
        self.playback.stop()    # Stop playback if active

        action = self._setlist['actions'][self._current_id]
        logger.info(action)

        await manager.broadcast(action, "action-config")
        await manager.broadcast(str(action['nbr']), "executing-action-nbr")

        cuelist: list(str) = []
        try:
            cuelist = self._setlist['actions'][self._current_id]['execution']['lights']['cuelist']
        except Exception:
            pass
        
        if action['type'] == "song": 
            #Create marker to easily identify where songs start
            self.recording.create_marker()

            if action.get('playback'):
                try:
                    self.playback.start(action['execution']['playback']['marker_name'])
                except Exception as e:
                    logger.error("Unable to start playback")
                    logger.debug(e)
                

        # Only release and start if cuelist differs from currently active
        if set(self.lights.get_active()) != set(cuelist):
            self.lights.release_active_cuelists()
            self.lights.start_cuelist(cuelist)



        self._current_id += 1
        return


    def prev_event(self, event_initiator:str = ""):
        logger.debug("Previous song triggered : %s", event_initiator)
        logger.error("NOT IMPLEMENTED")

    def goto_action(self, action_nbr: int):
        logger.debug("Going to action: " + action_nbr)

    def action_btn_pressed(self, btn_id:int, btn_initiator=""):
        logger.info(f"Executing song button {btn_id}")

    def get_next_song_id(self) -> int:
        """
        Returns song current song id. If no set is loaded -1
        """
        if not self._setlist:
            return -1

        action_arr = self._setlist['actions']

        search_id: int
        if self._current_id >= 0:
            search_id = self._current_id
        else: search_id = 0

        while True:
            logger.debug(f"Current: {self._current_id}, search: {search_id}")
            if len(action_arr) <= search_id:
                return -1
            elif action_arr[search_id].get("song_id"):
                return action_arr[search_id].get("song_id")
            else:
                search_id = search_id + 1
        

    def _reset_engine(self) -> None:
        """
        Resets engine state
        """
        logger.debug("Resetting engine")
        self._setlist = {}
        self._status = "idle"
        self._current_id = -1
        self.lights.release_active_cuelists(persistent=True)
        self.playback.stop(force_send=True)    # Send playback stop 