from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional, Sequence

class LightCommandShort(BaseModel):
    id: int
    name: str
    # class Config():
        # orm_mode = True
class LightCommandBase(BaseModel):
    name: str
    osc_path: str
    type: Optional[str]
    auto_release_ms: Optional[int]
    category: Optional[int]
    description: Optional[str]
    is_default: Optional[bool]

class LightCommandCreate(LightCommandBase):
    pass

class LightCommandUpdate(LightCommandBase):
    pass

class LightCommand(LightCommandBase):
    id: int

    class Config():
        orm_mode = True

class SongIdentity(BaseModel):
    id: int
    name: str

class LightCommandUsage(LightCommand):
    used_in: List[SongIdentity]