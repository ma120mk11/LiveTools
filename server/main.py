import asyncio
import uvicorn
from typing import List
from fastapi import FastAPI, Body ,HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import schemas, models, crud, live_engine
from device_manager import device_mgr
from websocket.connection_manager import manager
from database import SessionLocal, db_engine
from sqlalchemy.orm import Session
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from osc.osc_server import server
from sqlalchemy import update
from sqlalchemy.future import select
import json

# dictConfig(LogConfig)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=db_engine)

app = FastAPI(debug=True)
engine = live_engine.Engine()
server.start_osc_server()

async def start_osc():
    await engine.start_osc()
asyncio.create_task(start_osc())


origins = [
    "*"
    "http://localhost",
    "http://localhost:4200",
    "http://192.168.43.249:4200",
    "http://192.168.1.40:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Dependency
def get_db():
    # This will make sure the db session is always closed, even if an exception occurs
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#////////////////////////////////////////////////////////////////
#//                         USERS                              //
#////////////////////////////////////////////////////////////////
@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User], tags=["users"])
def read_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/user/{user_id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db,user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return


@app.put("/user/{user_id}", tags=["users"], status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id)
    return


#////////////////////////////////////////////////////////////////
#//                         SONGS                              //
#////////////////////////////////////////////////////////////////
@app.post('/songs/{song_id}/preview', response_model=schemas.Song, tags=["songs"])
async def preview_song_by_id(song_id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id)
    if not song.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
    
    song_dict = jsonable_encoder(song.first())

    exec = json.loads(db.query(models.Song.execution).filter(models.Song.id == song_id).scalar())
    logger.info(str(song.scalar()))

    song_dict['execution'] = exec
    song_dict['type'] = "song"
    song_dict['song_id'] = song_dict['id']
    song_dict.pop("id")

    await engine.preview_action(song_dict)


@app.post('/song', response_model=schemas.Song, tags=["song-library"])
def add_song(song: schemas.SongCreate, db: Session = Depends(get_db)):

    return crud.create_song(db, song)


@app.get('/songs', response_model=List[schemas.Song], tags=["song-library"])
def get_songs(
    skip: int=0, 
    limit: int=100,
    sort_by: str= "",
    sort_order: str="", 
    db: Session = Depends(get_db)
    ):

    songs = crud.get_songs(db,skip,limit, sort_by, sort_order)
    return songs


@app.get('/songs/{song_id}', response_model=schemas.Song, tags=["song-library"])
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = crud.get_song(db,song_id)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    return song


@app.delete("/songs/{song_id}", tags=["song-library"], status_code=status.HTTP_202_ACCEPTED)
def delete_song(song_id, db: Session = Depends(get_db)):
    db_song = crud.delete_song(db, song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="No such song")
    return

# @app.put('/songs/{song_id}')



@app.get('/artists', tags=["song-library"])
def get_artists(db: Session = Depends(get_db)):
    
    artist = schemas.Artist(
        name="Hurriganes",
        song_amount=2
    )

    return artist


# @app.delete('/songs/{id}', tags=["songs"], status_code=status.HTTP_204_NO_CONTENT)
# def delete_song_by_id(id: int, db: Session = Depends(get_db)):
#     db.query(models.Song).filter(models.Song.id == id).delete(synchronize_session=False)
#     db.commit()
#     return


#////////////////////////////////////////////////////////////////
#//                        ENGINE                              //
#////////////////////////////////////////////////////////////////
@app.post("/osc/maps/add/", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
def add_map(map: str):
    print("Trying to add " + map)
    server.addMap(map)
    return


# @app.post("/osc/send/", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
# def send_osc_msg(osc_address: str,value: float):
#     logging.debug("Sending OSC msg: %s . %f", osc_address, value)
#     engine.osc.send_osc_msg(osc_address,value)
#     return

# @app.get("/osc/server_ip", tags=["engine"])
# def get_server_ip():
#     return engine.osc.getServerIP()


@app.post("/engine/set/load", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def load_set(set_to_load: dict):
    logger.debug(set_to_load)
    await engine.load_setlist(set_to_load)
    return



@app.post("/engine/set/start", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
def start_set():
    if engine.get_status() != "is_running":
        engine.start_set()
    return

@app.post("/engine/set/next", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
def next_song():
    engine.next_event()
    return

@app.post("/engine/action/preview", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def test_action(action: dict):
    await engine.preview_action(action)

@app.post("/engine/action/preview/release", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
async def release_preview():
    await engine.release_preview()



@app.get("/engine/lights/active", tags=["engine", "lights"])
def get_active_cuelists():
    return engine.lights.get_active_cuelists()


@app.get("/engine/state", tags=["engine"])
def get_engine_status():
    return engine.get_status()


@app.get("/engine/next-lyrics", tags=["engine", "lyrics"])
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

    return "Start set or song to view lyrics"

#////////////////////////////////////////////////////////////////
#//                        DEVICES                             //
#////////////////////////////////////////////////////////////////

@app.get("/mixer/search")
def search_for_mixer():
    """Returns the IP of the first found mixer"""
    return engine.mixer.find_mixer()

@app.get("/devices/", response_model=List[schemas.OSCDevice], tags=["devices"])
def get_connected_devices():
    return device_mgr.get_connected()

@app.patch("/devices/{id}", response_model=schemas.OSCDevice, tags=["devices"])
async def device_config(id:int, request: schemas.OSCDeviceUpdate ):
    if request.ip:
        await device_mgr.set_ip(device_id=id, ip= request.ip)
    if request.receive_port:
        await device_mgr.set_receive_port(device_id=id, port=request.receive_port)
    if request.enabled is not None:
        await device_mgr.set_enabled(id, request.enabled)

# @app.get("/devices/test/{id}", tags=["devices"])
# async def test_device_connection(id:int):
#     is_connected = engine.recording.test_connection()
#     return await is_connected
    

@app.post('/songs/{id}/lyrics',
        tags=["songs"],
        status_code=status.HTTP_202_ACCEPTED
    )
def update_lyrics(id: int, lyrics: str = Body(...), db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == id)
    if not song.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
    song.update({'lyrics': lyrics})
    db.commit()
    return

@app.post('/songs/{song_id}/execution', status_code=status.HTTP_202_ACCEPTED)
def update_song_execution(song_id: int, execution: schemas.Execution, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id)
    if not song.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
    
    exec_str = jsonable_encoder(execution)
    
    song.update({'execution': json.dumps(exec_str)})

    db.commit()

    return


@app.put('/songs/{id}', 
        tags=["songs"],
        status_code=status.HTTP_202_ACCEPTED
    )
def update_song(
        id: int, 
        request: schemas.Song,
        db: Session = Depends(get_db)
    ):

    song = db.query(models.Song).filter(models.Song.id == id)
    if not song.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No song with id {id} found")
    song.update(request)
    db.commit()
    return


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # await engine.start_osc()
    await manager.connect(websocket, client_id)
    try:
        # send engine status to connected client:
        await manager.send_personal_message(websocket, engine.get_engine_state(), "engine-state")
        await manager.send_personal_message(websocket, jsonable_encoder(device_mgr.get_status()), "device-state")
        
        while True:
            data = await websocket.receive_text()
            if data == "next-song":
                await engine.next_event(client_id)
            elif data == "start-set":
                await engine.start_set()
                await manager.broadcast(f"engine:{engine.get_status()}")
            elif data.startswith("song-btn-press:"):
                btn_id = int(data.replace("song-btn-press:", ""))
                engine.action_btn_pressed(btn_id, client_id)
            
            else:
                await manager.send_personal_message(f"unsupported command: {data}", "error", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} disconnected", "notification")


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.34.249", port=8000)