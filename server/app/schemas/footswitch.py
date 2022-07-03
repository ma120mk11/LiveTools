from typing import List, Optional, Sequence
from pydantic import BaseModel


class ButtonBase(BaseModel):
    type: Optional[str]
    name: str
    btn_id: int
    has_led: bool
    action_cat: str
    action_id: str

class ButtonCreate(ButtonBase):
    pass

class ButtonUpdate(ButtonBase):
    pass

class Button(ButtonBase):
    id: int
    fs_id: str

    class Config():
        orm_mode = True



class FootswitchBase(BaseModel):
    id: str
    name: str
    is_enabled: bool
    description: Optional[str]

class Footswitch(FootswitchBase):
    buttons: Sequence[Button]

    class Config():
        orm_mode = True

class FootswitchCreate(FootswitchBase):
    ...

class FootswitchUpdate(FootswitchBase):
    ...


class ButtonChange(BaseModel):
    fs_id: str
    btn_id: int
    state: bool