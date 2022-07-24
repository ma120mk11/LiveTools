from datetime import datetime
import json
import logging
from typing import Any, Dict, Optional, Union
from unicodedata import name
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas.light_cmd import LightCommand
from app.schemas.song import Execution, ExecutionUpdate, Song, SongCreate, SongUpdate
from app.models.song import Song as SongModel
from app.models.light_cmd import LightCommand as LightCommandModel
from app.crud.crud_light_cmd import light_cmd
logger = logging.getLogger(__name__)


class CRUDSong(CRUDBase[Song, SongCreate, SongUpdate]):

    def get_song(self, db: Session, song_id: int, include_lyrics: bool = True) -> Song:
        return self._transform_song(db.query(SongModel).filter(SongModel.id == song_id).first(), db=db, include_lyrics=include_lyrics)

    def get_songs(self, db: Session, skip: int=0, limit: int=100, sort_by="", sort_order="", include_hidden:bool=True, include_lyrics: bool = True):
        if include_hidden:
            songs = db.query(SongModel).offset(skip).limit(limit).all()
        else:
            songs = db.query(SongModel).filter(or_(SongModel.hidden == None, SongModel.hidden == False)).offset(skip).limit(limit).all()
    
        for song in songs:
            song = self._transform_song(song, db=db, include_lyrics=include_lyrics)
        return songs

    def _transform_song(self, song: Song, db: Session, include_lyrics: bool = True) -> Song:
        # logger.info(type(song.execution))
        if not isinstance(song.execution, str):
            logger.info(f"Getting song: {song.title} ({song.id})")

            logger.info(song.execution)
        else:
            song.execution = json.loads(song.execution)
        new_cuelist = []

        if song.execution['lights']['cuelist']:
            for cue in song.execution['lights']['cuelist']:
                if isinstance(cue, int):
                    c = light_cmd.get(db=db, id=cue)
                    if c:
                        new_cuelist.append({"id": c.id, "name": c.name})
                    else:
                        # TODO: Suitable behavior for handling cue not found
                        logger.error(f"Could not find Cuelist with id {cue}")
                    
                else:
                    new_cuelist.append(cue)
            song.execution['lights']['cuelist'] = new_cuelist
        if isinstance(song.lead_singer, str):
            song.lead_singer = song.lead_singer.split(",")

        if not include_lyrics:
            song.lyrics = ""

        return song

    def create_song(self, db: Session, song: SongCreate):
        temp: dict = song.dict()
        temp.pop("execution")
        temp.pop("lead_singer")

        temp['created'] = datetime.now()    #TODO: Move to DB Shema
        temp['lead_singer'] = ",".join(song.lead_singer)
        temp['execution'] = json.dumps(jsonable_encoder(song.execution))

        db_song = SongModel(**temp)
        db.add(db_song)
        db.commit()
        db.refresh(db_song)

        return self._transform_song(db_song, db=db)

    def delete_song(self, db: Session, song_id: int):
        db_song = db.query(SongModel).filter(SongModel.id == song_id).delete(synchronize_session=False)
        db.commit()
        return db_song


    def update_tempo(self, db: Session, id: int, tempo_in):
        song = db.query(SongModel).filter(SongModel.id == id)
        if not song.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
        song.update({'tempo': tempo_in})
        db.commit()
        return

        
    def update_song_execution(self, id: int, execution_in: ExecutionUpdate, db: Session):
        song = db.query(SongModel).filter(SongModel.id == id)
        if not song.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
        
        exec_str = jsonable_encoder(execution_in)
        song.update({'execution': json.dumps(exec_str)})
        db.commit()
        return

song = CRUDSong(SongModel)