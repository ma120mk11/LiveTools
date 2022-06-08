from pydantic import BaseModel, HttpUrl
from datetime import datetime

from typing import List, Optional, Sequence, Union

# class DeviceState(str, Enum):
#     disconnected = "disconnected"
#     connected = "connected"
#     disabled = "disabled"

class OSCDeviceUpdate(BaseModel):
    ip: Optional[str]
    receive_port: Optional[int]
    enabled: Optional[bool]


class OSCDeviceBase(BaseModel):
    name: str
    type: str
    ip:  str
    send_port: Optional[int]
    receive_port: Union[int, None]
    enabled: Optional[bool]

class OSCDevice(OSCDeviceBase):
    state: str
    id: int
