from pydantic import BaseModel, HttpUrl
from datetime import datetime

from typing import List, Optional, Sequence

class LightCommandBase(BaseModel):
    name: str
    osc_path: str
    type: Optional[str]
    auto_release_ms: Optional[int]
    category: Optional[int]

class LightCommandCreate(LightCommandBase):
    pass

class LightCommandUpdate(LightCommandBase):
    pass

class LightCommand(LightCommandBase):
    id: int

    class Config():
        orm_mode = True