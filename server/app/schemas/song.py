from pydantic import BaseModel, HttpUrl
from datetime import datetime

from typing import List, Optional, Sequence

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

