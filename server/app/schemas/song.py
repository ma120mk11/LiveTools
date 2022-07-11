from pydantic import BaseModel
from datetime import datetime
from app.schemas.light_cmd import LightCommandShort
from typing import List, Optional, Union


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

class LightExecutionBase(BaseModel):
    blackout: Optional[bool]

class LightExecution(LightExecutionBase):
    blackout: Optional[bool]
    cuelist: Optional[List[Union[LightCommandShort, str]]]

class LightExecutionUpdate(BaseModel):
    cuelist: Optional[List[int]]

class ExecutionBase(BaseModel):
    playback: PlaybackExecution
    lights: LightExecution
    audio: AudioExecution


class ExecutionCreate(ExecutionBase):
    ...
class ExecutionUpdate(ExecutionBase):
    playback: PlaybackExecution
    lights: LightExecutionUpdate
    audio: AudioExecution

class Execution(ExecutionBase):
    ...


class SongBase(BaseModel):
    title: str
    artist: str
    tempo: Optional[int]
    lyrics: Optional[str]
    duration: Optional[int]
    lead_singer: Optional[List[str]]
    key: Optional[str]
    playback: Optional[bool]
    description: Optional[str]
    execution: Optional[Execution]

class SongCreate(SongBase):
    pass

class SongUpdate(SongBase):
    pass

class Song(SongBase):
    id: int
    last_played: Optional[datetime]
    created: Optional[datetime]
    version: Optional[int]
    hidden: Optional[bool]

    class Config:
        orm_mode = True


class SongAction(Song):
    type: str = "song"