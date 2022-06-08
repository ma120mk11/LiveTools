from pydantic import BaseModel
from enum import Enum


class Artist(BaseModel):
    name: str
    song_amount: int
