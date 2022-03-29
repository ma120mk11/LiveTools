from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    artist = Column(String)
    lyrics = Column(String)
    tempo = Column(Integer)
    duration = Column(Integer)
    lead_singer = Column(String)
    key = Column(String)
    version = Column(Integer)
    playback = Column(Boolean)
    hidden = Column(Boolean)
    tags = Column(String)
    created = Column(DateTime)
    last_played = Column(DateTime)
    description = Column(String)
    execution = Column(JSON)      # Store execution properties as string for now


class Setlist(Base):
    __tablename__ = "setlists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    