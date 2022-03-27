from datetime import datetime
from sqlalchemy.orm import Session
import models, schemas

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
    return db.query(models.Song).filter(models.Song.id == song_id).first()

def get_songs(db: Session, skip: int=0, limit: int=100, sort_by="", sort_order=""):
    return db.query(models.Song).offset(skip).limit(limit).all()

def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(
        created=datetime.now(), **song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

def delete_song(db: Session, song_id: int):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).delete(synchronize_session=False)
    db.commit()
    return db_song