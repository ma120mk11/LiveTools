from typing import List
from fastapi import FastAPI, HTTPException, Depends, status, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import schemas, models, crud, live_engine
from device_manager import DeviceManager, device_mgr
from websocket.connection_manager import manager
from database import SessionLocal, db_engine
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging
from logging.config import dictConfig
import LogConfig
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder


# dictConfig(LogConfig)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=db_engine)

app = FastAPI(debug=True)
engine = live_engine.Engine()

# engine.start_osc()
# devices = DeviceManager()

origins = [
    "http://localhost",
    "http://localhost:4200",
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
    engine.osc.addMap(map)
    return


@app.post("/osc/send/", status_code=status.HTTP_202_ACCEPTED, tags=["engine"])
def send_osc_msg(osc_address: str,value: float):
    logging.debug("Sending OSC msg: %s . %f", osc_address, value)
    engine.osc.send_osc_msg(osc_address,value)
    return

@app.get("/osc/server_ip", tags=["engine"])
def get_server_ip():
    return engine.osc.getServerIP()


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
    engine.end_set()
    return


@app.get("/engine/lights/active", tags=["engine", "lights"])
def get_active_cuelists():
    return engine.lights.get_active_cuelists()


@app.get("/engine/state", tags=["engine"])
def get_engine_status():
    return engine.get_status()

#////////////////////////////////////////////////////////////////
#//                        DEVICES                             //
#////////////////////////////////////////////////////////////////

@app.get("/devices/", response_model=List[schemas.OSCDevice], tags=["devices"])
def get_connected_devices():
    return device_mgr.get_connected()

@app.patch("/devices/{id}", response_model=schemas.OSCDevice, tags=["devices"])
async def device_config(id:int, request: schemas.OSCDeviceUpdate ):
    if request.ip:
        await device_mgr.set_ip(device_id=id, ip= request.ip)
    if request.receive_port:
        await device_mgr.set_receive_port(device_id=id, port=request.receive_port)

@app.post("/devices/connect", status_code=status.HTTP_202_ACCEPTED, tags=["devices"])
def connect_device(device: schemas.OSCDeviceBase):
    
    if not device_mgr.connect(device):
        raise HTTPException(detail="Error connecting device")
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



html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>LiveTools</title>
        </head>
        <body>
            <h1>LiveTools Websocket</h1>
            <h2>Your ID: <span id="ws-id"></span></h2>
            <button onclick="next('start-set')">Start set</button>
            <button onclick="next('next-song')">Next</button>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
                var client_id = browserDetect() + "-" + getRandomInt(1,99);
                document.querySelector("#ws-id").textContent = client_id;
                var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                function sendMessage(event) {
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }
                function next(command){
                    ws.send(command)
                }
                function browserDetect(){
                 
                    let userAgent = navigator.userAgent;
                    let browserName;
                    
                    if(userAgent.match(/chrome|chromium|crios/i)){
                        browserName = "chrome";
                    }else if(userAgent.match(/firefox|fxios/i)){
                        browserName = "firefox";
                    }  else if(userAgent.match(/safari/i)){
                        browserName = "safari";
                    }else if(userAgent.match(/opr\//i)){
                        browserName = "opera";
                    } else if(userAgent.match(/edg/i)){
                        browserName = "edge";
                    }else{
                        browserName="No browser detection";
                    }
                    return browserName
                }
                function getRandomInt(min, max) {
                    min = Math.ceil(min);
                    max = Math.floor(max);
                    return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
                }
            </script>
        </body>
    </html>
"""





# manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)



@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await engine.start_osc()
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

