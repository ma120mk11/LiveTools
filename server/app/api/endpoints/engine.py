import json
import asyncio
import logging
from typing import List
from fastapi import APIRouter ,HTTPException, Depends, status
from app import dependencies
from fastapi import APIRouter
from app.osc.osc_server import server
from sqlalchemy.orm import Session
from app.models.song import Song as SongModel
from fastapi.encoders import jsonable_encoder
from app.dependencies import get_db
from app.schemas.song import Song
from app.crud import song as crud
from app.live_engine import Engine, engine

logger = logging.getLogger(__name__)

router = APIRouter()

# engine = live_engine.Engine()

server.start_osc_server()

async def start_osc():
    await engine.start_osc()
asyncio.create_task(start_osc())


@router.post('/songs/{song_id}/preview', response_model=Song, tags=["songs"])
async def preview_song_by_id(song_id: int, db: Session = Depends(dependencies.get_db)):
    song = db.query(SongModel).filter(SongModel.id == song_id).first()
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
    
    song_dict = jsonable_encoder(song)

    exec = json.loads(db.query(SongModel.execution).filter(SongModel.id == song_id).scalar())
    # logger.info(str(song.scalar()))

    song_dict['execution'] = exec
    song_dict['type'] = "song"
    song_dict['song_id'] = song_dict['id']
    song_dict.pop("id")

    await engine.preview_action(song_dict)


#////////////////////////////////////////////////////////////////
#//                        ENGINE                              //
#////////////////////////////////////////////////////////////////
@router.post("/osc/maps/add/", status_code=status.HTTP_202_ACCEPTED, tags=["osc"])
def add_map(map: str):
    print("Trying to add " + map)
    server.addMap(map)
    return


@router.post("/set/load", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def load_set(set_to_load: dict):
    logger.debug(set_to_load)
    await engine.load_setlist(set_to_load)
    return



@router.post("/set/start", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
def start_set():
    if engine.get_status() != "is_running":
        engine.start_set()
    return

@router.post("/set/next", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
def next_song():
    engine.next_event()
    return

@router.post("/set/insert-speech", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def add_speech_next():
    """
    Adds a speech as the next action
    """
    # speech = {
    #     "type": "speech",
    #     "duration": 5,
    #     "execution": {
    #         "lights": {
    #             "cuelist": ["speaking"]
    #         }
    #     }
    # }
    # await engine.add_to_cue(actions=[speech])
    await engine.add_speech_to_cue()
    return

@router.post("/set/prev", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def prev_song():
    await engine.prev_event()
    return

@router.post("/reset", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def reset_engine():
    await engine._reset_engine(notify_end_set=True)
    return



@router.post("/cue/add", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def add_songs_by_id_to_cue(song_ids: List[int], db: Session = Depends(get_db)):
    songs = []

    for song_id in song_ids:

        if song_id == 1000:
            song = {
                "type": "speech",
                "duration": 5,
                "execution": {
                    "lights": {
                        "cuelist": ["speaking"]
                    }
                }
            }
    
        else:
            song = jsonable_encoder(crud.get_song(db, song_id))
            song['type'] = "song"
            # TODO: Move to crud
            if "lyrics" in song:
                song.pop("lyrics")

        songs.append(song)

    await engine.add_to_cue(songs)

    return




@router.post("/action/preview", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def test_action(action: dict):
    await engine.preview_action(action)

@router.post("/action/preview/release", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def release_preview():
    await engine.release_preview()


@router.post("/action/blackout", status_code=status.HTTP_202_ACCEPTED, tags=["engine", "lights"])
async def blackout():
    engine.lights.blackout()


@router.get("/lights/active", tags=["engine", "lights"])
def get_active_cuelists():
    return engine.lights.get_active_cuelists()

@router.get("/lights/cuelists", tags=["engine", "lights"], deprecated=True)
def get_cuelists():
    return engine.lights.get_cuelist()

@router.get("/state", tags=["engine"])
def get_engine_status():
    return engine.get_status()


@router.get("/next-lyrics", tags=["engine", "lyrics"])
def get_lyrics_for_next_song(lookahead: int=3, db: Session = Depends(get_db)):
    
    song_id = engine.get_next_song_id()
    logger.debug("Next song id: " + str(song_id))
    if song_id >= 0:
        song = crud.get_song(db, song_id)
        if song is None:
            return "No lyrics available"
        else: 
            if song.lyrics:
                return song.lyrics
            else:
                return "No lyrics available"

    return "Start set or song to view lyrics"

