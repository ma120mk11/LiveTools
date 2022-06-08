import logging
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import crud_song as crud
from app.models.song import Song as SongModel
from app.schemas.song import Song, SongCreate, Execution
from app import dependencies

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=List[Song])
def get_songs(
        include_hidden: bool = False,
        include_lyrics: bool = True,
        skip: int=0, 
        limit: int=100,
        sort_by: str= "",
        sort_order: str="", 
        db: Session = Depends(dependencies.get_db)
    ):
    logger.info("include hidden: " + str(include_hidden))
    songs = crud.song.get_songs(db,skip,limit, sort_by, sort_order, include_hidden, include_lyrics=include_lyrics)
    return songs



@router.get('/{song_id}', response_model=Song)
def get_song(
        song_id: int, 
        db: Session = Depends(dependencies.get_db)
):
    song = crud.song.get_song(db,song_id)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song



@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_song(
        id: int, 
        request: Song,
        db: Session = Depends(dependencies.get_db)
    ):

    song = db.query(SongModel).filter(SongModel.id == id)
    if not song.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
    song.update(request)
    db.commit()
    return



@router.post('/', response_model=Song)
def add_song(song: SongCreate, db: Session = Depends(dependencies.get_db)):

    return crud.create_song(db, song)


@router.delete("/{song_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_song(song_id, db: Session = Depends(dependencies.get_db)):
    db_song = crud.song.delete_song(db, song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="No such song")
    return



@router.post('/{id}/tempo', status_code=status.HTTP_202_ACCEPTED)
def set_song_tempo(id: int, tempo: int = Body(...), db: Session = Depends(dependencies.get_db)):
    '''The song tempo will not be updated for everybody'''
    crud.song.update_tempo(id=id, tempo_in=tempo, db=db)
    return



@router.post('/{id}/lyrics', status_code=status.HTTP_202_ACCEPTED)
def update_lyrics(id: int, lyrics: str = Body(...), db: Session = Depends(dependencies.get_db)):
    song = db.query(SongModel).filter(SongModel.id == id)
    if not song.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
    song.update({'lyrics': lyrics})
    db.commit()
    return



@router.post('/{song_id}/execution', status_code=status.HTTP_202_ACCEPTED)
def update_song_execution(song_id: int, execution: Execution, db: Session = Depends(dependencies.get_db)):
    song = crud.song.update_song_execution(id=song_id, execution_in=execution,db=db)

    return

