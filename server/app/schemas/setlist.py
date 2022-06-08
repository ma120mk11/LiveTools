from pydantic import BaseModel, HttpUrl
from typing import List, Optional



class FXModel(BaseModel):
    enabled: Optional[bool]

class AudioExecution(BaseModel):
    fx1: FXModel
    fx2: FXModel
    fx3: FXModel
    fx4: FXModel
    channel_mutes: Optional[List[int]]

class PlaybackExecution(BaseModel):
    marker_name: Optional[str]

class LightExecution(BaseModel):
    blackout: Optional[bool]
    cuelist: Optional[List[str]]

class Execution(BaseModel):
    playback: PlaybackExecution
    lights: LightExecution
    audio: AudioExecution

class SongAction(BaseModel):
    song_id: int
    type: str
    title: str
    artist: str
    version: int
    playback: bool
    execution: Execution

class SetlistMetadata(BaseModel):
    gig_name: str
    set_nbr: int
    date: str
    name: str

class SetlistAction(BaseModel):
    type: str
    nbr: Optional[int]
    execution: str

class Setlist(BaseModel):
    id: int
    metadata: SetlistMetadata
    name: str
    actions: List[SetlistAction]

