from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Union

from app.schemas.song import Song, SongAction

class SetlistAction(BaseModel):
    ...

class SetlistBase(BaseModel):
    name: str
    comments: Optional[str]
    tags: Optional[str]
    setup: Optional[str]
    tags: Optional[str]
    actions: List[int]

class SetlistCreate(SetlistBase):
    ...

class SetlistUpdate(SetlistBase):
    id: int
    created: datetime
    last_played: datetime


class Setlist(SetlistBase):
    id: int
    created: datetime
    last_played: datetime
    class Config:
        orm_mode = True

class SetlistFull(Setlist):
    actions: List[Union[SongAction, dict]]
