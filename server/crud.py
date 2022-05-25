from datetime import datetime
import json
from sqlalchemy import null, or_
from sqlalchemy.orm import Session
import models, schemas
from fastapi.encoders import jsonable_encoder


#////////////////////////////////////////////////////////////////
#//                         USERS                              //
#////////////////////////////////////////////////////////////////
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "_enigma"
    db_user = models.User(
        name = user.name,
        hashed_password = fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return db_user

def update_user(db: Session, user_id: int):
    pass


#////////////////////////////////////////////////////////////////
#//                         SONGS                              //
#////////////////////////////////////////////////////////////////
def get_song(db: Session, song_id: int):
    return transform_song(db.query(models.Song).filter(models.Song.id == song_id).first())

def get_songs(db: Session, skip: int=0, limit: int=100, sort_by="", sort_order="", include_hidden:bool=True, include_lyrics: bool = True):
    if include_hidden:
        songs = db.query(models.Song).offset(skip).limit(limit).all()
    else:
        print("Do not include hidden songs")
        # songs = db.query(models.Song).filter(models.Song.hidden == None).offset(skip).limit(limit).all()
        songs = db.query(models.Song).filter(or_(models.Song.hidden == None, models.Song.hidden == False)).offset(skip).limit(limit).all()

    for song in songs:
        if not include_lyrics:
            if song.lyrics:
                song.lyrics = ""
            
        song = transform_song(song)
    return songs

def transform_song(song: models.Song):
    song.execution = json.loads(song.execution)
    song.lead_singer = song.lead_singer.split(",")
    return song

def create_song(db: Session, song: schemas.SongCreate):
    exec = json.dumps(jsonable_encoder(song.execution))
    singers = ",".join(song.lead_singer)

    temp: dict = song.dict()
    temp.pop("execution")
    temp.pop("lead_singer")

    temp['created'] = datetime.now()
    temp['lead_singer'] = ",".join(song.lead_singer)
    temp['execution'] = json.dumps(jsonable_encoder(song.execution))

    db_song = models.Song(**temp)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)

    return transform_song(db_song)

def delete_song(db: Session, song_id: int):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).delete(synchronize_session=False)
    db.commit()
    return db_song