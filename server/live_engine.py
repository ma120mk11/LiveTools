from datetime import datetime
import logging
from typing import List
from osc.ligths import OSCLights
from osc.playback import OSCPlayback
from osc.mixer import OSCMixer
from websocket.connection_manager import manager
from osc.recording import OSCRecoding
import time

logger = logging.getLogger(__name__)

class Engine():
    _setlist = {}
    _cuelist = []
    _status = "stopped"
    ##### Action ID
    # -1 : Stopped
    # -2 : Preview
    _current_action_id = -1
    _current_action: dict = {}
    _state_savepoint: dict
    _in_preview: bool = False
    _set_info: dict = { "actions": 0, "started_on": 0}
    # _started_on: datetime = 0

    def __init__(self):
        logger.info("Engine initializing")
        self.recording = OSCRecoding()
        self.lights = OSCLights()
        self.playback = OSCPlayback()
        self.mixer = OSCMixer()

    async def start_osc(self):
        logger.info("Connecting all OSC devices...")
        await self.mixer.connect("192.168.1.2", 10024)
        await self.lights.connect("192.168.1.5", 8887)
        # await self.lights.connect("192.168.1.6", 8887)  # Wireless
        await self.recording.connect("192.168.1.122", 3819)
        await self.playback.connect("192.168.1.6", 3819)


    def get_status(self) -> str:
        return self._status

    def get_engine_state(self) -> dict:
        """
        Returns current engine state
            setlist:
            action_id: Current executing action. 
                -1: engine is stopped
                -2: action preview mode
            status:
        """

        action_id = int
        if self._in_preview:
            action_id = -2
        else:
            action_id = self._current_action_id

        return {
            "setlist": self._setlist,
            "action_id": action_id,
            "current_action": self._current_action,
            "status": self._status, 
            "set_started_on": str(self._set_info['started_on'])
        }

    async def load_setlist(self, set: dict):
        """
        Loads a set
        Releases preview if active
        """
        logger.info("Loading setlist: %s", set['name'])

        count = 0
        for count, action in enumerate(set['actions']):
            action['nbr'] = count

        self._set_info['actions'] = count+1

        # TODO: How to handle loading a setlist if engine is running
        await self._reset_engine()

        self._setlist = set
        await manager.broadcast(self._setlist, "load-set")
        logger.info("Loaded set with %i actions", count+1)


    async def start_set(self):
        """Starts the loaded set"""
        # No set loaded
        if not self._setlist:
            logger.error("Unable to start set: No set loaded")
            return 
        if self._current_action_id >= 0:
            logger.error("Unable to start set: A set is already running")
            return

        # self._current_action_id = 0            # First action
        self._status = "set_running"
        self._set_info['started_on'] = datetime.now()
    
        self.mixer.mute_all_fx()        # Mute when starting set

        await self.recording.record()

        # Set frontlights and leave them on for rest of the set
        self.lights.start_cuelist(["frontlights"], persistent=True)

        await manager.broadcast(str(self._set_info['started_on']), "set-started")
        # Automatically start action 0
        await self.next_event("engine")


    async def end_set(self) -> None:
        """
        Ends a running set
        """
        logger.info("Ending set...")

        await manager.broadcast("end-set", "end-set")

        self.lights.release_active_cuelists()
        await self.recording.stop_recording()

        await self._reset_engine()


    async def _execute_action(self, action:dict, preview=False):
        logger.debug(action)
        self._current_action = action
        await self.playback.stop()    # Stop playback if active

        await manager.broadcast(action, "action-config")
        # await manager.broadcast(str(action.get('nbr',-2)), "executing-action-nbr")
        if self._in_preview:
            await manager.broadcast(str(-2), "executing-action-nbr")
        else:
            await manager.broadcast(str(self._current_action_id), "executing-action-nbr")

        cuelist: list(str) = []
        try:
            cuelist = action['execution']['lights']['cuelist']
            if cuelist == None:
                cuelist = [""]
        except Exception:
            logger.error("Action doesn't contain a cuelist")
        
        if action['type'] == "song": 
            if not preview:
                #Create marker to easily identify where songs start
                self.recording.create_marker()

            if action.get('playback'):
                try:
                    self.playback.start(action['execution']['playback']['marker_name'])
                except Exception as e:
                    logger.error("Unable to start playback")
                    logger.debug(e)
                    await manager.broadcast("Error starting playback")
                
        if action['type'] == "speech":
            self.mixer.mute_all_fx()

        if action["execution"].get('audio'):
            self.mixer.set_fx_mutes(action["execution"]['audio'])

        # Only release and start if cuelist differs from currently active
        if set(self.lights.get_active()) != set(cuelist):
            self.lights.release_active_cuelists()
            self.lights.start_cuelist(cuelist)

        return



    async def next_event(self, event_initiator:str = ""):
        logger.info("Next event triggered by %s", event_initiator)

        # Check that engine is running
        if self._current_action_id == -2:
            await manager.broadcast("Release preview first", "notification-warning")
            logger.info("Set is not started")
            return
        
        self._current_action_id += 1
        
        logger.debug("Current action nbr: %i, of %i total", self._current_action_id, len(self._setlist['actions']))

        if self._current_action_id >= len(self._setlist['actions']):
            await self.end_set()
            return

        action = self._setlist['actions'][self._current_action_id]
        
        await self._execute_action(action, preview=False)


        return


    async def prev_event(self, event_initiator:str = ""):
        logger.debug("Previous song triggered : %s", event_initiator)
        

        # Check that engine is running
        if self._current_action_id == -2:
            await manager.broadcast("Release preview first", "notification-warning")
            logger.info("Set is not started")
            return
        
        if self._current_action_id == 0:
            return

        self._current_action_id -= 1
        
        logger.debug("Current action nbr: %i, of %i total", self._current_action_id, len(self._setlist['actions']))

        if self._current_action_id >= len(self._setlist['actions']):
            await self.end_set()
            return

        action = self._setlist['actions'][self._current_action_id]
        
        await self._execute_action(action, preview=False)

        return


    def goto_action(self, action_nbr: int):
        logger.debug("Going to action: " + action_nbr)

    def action_btn_pressed(self, btn_id:int, btn_initiator=""):
        logger.info(f"Executing song button {btn_id}")

    def get_next_song_id(self) -> int:
        """
        Returns current song id, if not a song it returns the next song id. If not available -1
        """
        logger.info("In preview: " + str(self._in_preview))
        if self._in_preview:
            logger.debug(self._current_action)
            return self._current_action.get('song_id', -1)

        if not self._setlist:
            return -1

        action_arr = self._setlist['actions']

        search_id: int
        if self._current_action_id >= 0:
            search_id = self._current_action_id
        else: search_id = 0

        while True:
            logger.debug(f"Current setlist action nbr: {self._current_action_id}, search: {search_id}")
            if len(action_arr) <= search_id:
                return -1
            elif action_arr[search_id].get("id"):
                return action_arr[search_id].get("id")
            else:
                search_id = search_id + 1


    async def preview_action(self, action: dict):
        """
        Overrides current engine state
        """
        logger.info("Action preview initiated")
        self._in_preview = True
        self._status = "preview"
        self._state_savepoint = self.get_engine_state()

        # Set frontlights
        self.lights.start_cuelist(["frontlights"], persistent=True)

        await self._execute_action(action, preview=True)


    async def add_to_cue(self, actions: List[dict]):
        """
        Adds action to song cue
        """
        if self._setlist:
            for action in actions:
                action['isCueItem'] = True

        logger.debug("Adding songs to cue...")

        if self._setlist:
            i = 1
            if self._current_action_id > 0:
                i = self._current_action_id + 1

            for action in actions:
                logger.info("Inserting at index " + str(i))
                self._setlist['actions'].insert(i, action)
                i = i + 1

            # Recalculate action nbrs
            count = 0
            for count, action in enumerate(self._setlist['actions']):
                action['nbr'] = count

            self._set_info['actions'] = count+1

        else:
            setlist = {}
            setlist['name'] = "Cue"
            setlist['actions'] = actions

            await self.load_setlist(setlist)

            await self.start_set()

        await manager.broadcast(self._setlist, "load-set")
        await manager.broadcast(str(self._current_action_id), "executing-action-nbr")

    async def add_action_next(self, actions: List[dict]):
        """
        Adds action to song cue
        """
        if self._setlist:
            for action in actions:
                action['isCueItem'] = True

        logger.debug("Adding songs to cue...")

        if self._setlist:
            i = 1
            if self._current_action_id > 0:
                i = self._current_action_id + 1

            for action in actions:
                logger.info("Inserting at index " + str(i))
                self._setlist['actions'].insert(i, action)
                i = i + 1

            # Recalculate action nbrs
            count = 0
            for count, action in enumerate(self._setlist['actions']):
                action['nbr'] = count

            self._set_info['actions'] = count+1

        else:
            setlist = {}
            setlist['name'] = "Cue"
            setlist['actions'] = actions

            await self.load_setlist(setlist)

            await self.start_set()

        await manager.broadcast(self._setlist, "load-set")
        await manager.broadcast(str(self._current_action_id), "executing-action-nbr")




    async def release_preview(self):
        """
        Releses current preview (if any)
        Sets engine state to the state before priview was initiated (if any)
        Starts frontlights and leaves them on.
        """
        logger.info("Action preview release initiated")
        
        if not self._in_preview:
            logger.info("Engine is not in preview")

        self._in_preview = False

        #Started set
        if self._current_action_id > -1:
            self._status = "set_running"
            await self.next_event("Preview release")
        #Set loaded, but not started
        elif self._setlist:
            await manager.broadcast(self._current_action_id, "executing-action-nbr")
        else:
            # Don't reset persistent lights for now, to avoid blackout
            await self._reset_engine(persistent=False)

            await manager.broadcast(self._current_action_id, "executing-action-nbr")
        

    async def _reset_engine(self, persistent=False, notify_end_set=False) -> None:
        """
        Resets engine state
        """
        logger.debug("Resetting engine")
        self._setlist = {}
        self._status = "idle"
        self._current_action_id = -1
        self._current_action = {}
        self._in_preview = False
        self.mixer.mute_all_fx()
        self.lights.release_active_cuelists(persistent=persistent)
        await self.playback.stop(force_send=True)    # Send playback stop 
        await manager.broadcast(str(self._current_action_id), "executing-action-nbr")
        if notify_end_set:
            await manager.broadcast("end-set", "end-set")
