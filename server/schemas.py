from ipaddress import IPv4Address
from turtle import st
from typing import List, Optional, Union
from pydantic import BaseModel
from enum import Enum

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




class DeviceState(str, Enum):
    disconnected = "disconnected"
    connected = "connected"
    disabled = "disabled"

class OSCDeviceUpdate(BaseModel):
    ip: Optional[str]
    receive_port: Optional[int]


class OSCDeviceBase(BaseModel):
    name: str
    type: str
    ip:  str
    send_port: Optional[int]
    receive_port: Union[int, None]

class OSCDevice(OSCDeviceBase):
    state: str
    id: int





class ConfigurationBase(BaseModel):
    onyx_ip: str
    controller_ip: str
    daw_ip: str

class Configuration(ConfigurationBase):
    pass




class SongBase(BaseModel):
    title: str
    artist: str
    tempo: Optional[int]
    lyrics: Optional[str]
    duration: Optional[int]
    lead_singer: Optional[str]
    key: Optional[str]

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int

    class Config:
        orm_mode = True



class Setlist(BaseModel):
    id: int
    songs: List[Song] = []

    class Config():
        orm_mode = True



class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    name: str

    class Config:
        orm_mode = True



class Artist(BaseModel):
    name: str
    song_amount: int