
from http.client import HTTPException
import json
import logging
import time
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from app.db.session import SessionLocal
from app.websocket.connection_manager import manager
from app.live_engine import engine
from app.schemas.footswitch import ButtonChange, Footswitch, FootswitchCreate, ButtonCreate, Button, ButtonUpdate
from app.models.footswitch import Button as ButtonModel, Footswitch as FootswitchModel
from app import crud, dependencies
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter()


actions = [
    {"name": "Next", "action_cat": "engine", "action_id": "next"},
    {"name": "Blackout", "action_cat": "lights", "action_id": "blackout"},
    {"name": "Strobe", "action_cat": "lights", "action_id": "strobe"},
    {"name": "Blind", "action_cat": "lights", "action_id": "blind"},
    {"name": "Add speech", "action_cat": "engine", "action_id": "speech-add"},
    {"name": "Speech", "action_cat": "engine", "action_id": "speech-next"},
    {"name": "Song btn 1", "action_cat": "song", "action_id": "btn-1"},
    {"name": "Song btn 2", "action_cat": "song", "action_id": "btn-2"},
]

@router.websocket("/{client_id}")
async def websocket_footswitch(
    websocket: WebSocket,
    client_id: str,
) -> None:

    await connect(websocket, client_id)

    config = await websocket.receive_json()
    if not config['type'] == "config":
        logger.error("Could not connect footswitch: config error")
        websocket.close()
        return
    
    db = SessionLocal()
    try:
        fs = db.query(FootswitchModel.id).filter(FootswitchModel.id == config['data']['fs_id']).first()
        if not fs:
            logger.info("Footswitch not found in db")
    except Exception as e:
        logger.error("Could not connect footswitch: config error")
    finally:
        db.close()

    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"Footswitch {client_id}: {data}")
            
            try:
                data = json.loads(data)
            except Exception as e:
                logger.error("Data is not in JSON format")
                continue

            db: Session
            
            if (data['type'] == "btn-change") and (data['data']['state'] == 1):
                try:
                    await execute(
                        data=data,
                        db=SessionLocal(),
                        client_id=client_id,
                        fs_id=data['data']['fs_id'],
                        btn_id=data['data']['btn_id']
                    )
                except Exception as e:
                    logger.error("An exception occured")
                finally:
                    db.close()
            
    except WebSocketDisconnect as e:
        logger.error("Disconneced")
        # Notify web clients
        await manager.broadcast(f"Footswitch {client_id} disconnected", "notification")
    except Exception as e:
        logger.error("An unknown error occured: ")
        await manager.broadcast(f"Footswitch {client_id} disconnected", "notification")


async def connect(websocket: WebSocket, client_id: str):
    await websocket.accept()
    logger.info("Footswitch connected: %s", client_id)



async def execute(db: Session, data: dict, btn_id: int, fs_id: str, client_id="unknown") -> None:
    btn_conf = {}
    # btn_id = data['data']['btn_id']
    # fs_id = data['data']['fs_id']

    btn_conf = db.query(ButtonModel).filter(ButtonModel.btn_id == btn_id).filter(ButtonModel.fs_id == fs_id).first()
    if not btn_conf:
        logger.error("Button config not found")
        return

    # Button actions ///////////////////////////////////////////////////
    category = btn_conf.action_cat
    action = btn_conf.action_id
    # engine
    if category == "engine":
        # next
        if action == "next":
            await engine.next_event(db=db, event_initiator=f"footswitch: {client_id}")
        # Speech
        elif action == "speech-add":
                await engine.add_speech_to_cue()
        # Speech
        elif action == "speech-next":
                await engine.add_speech_to_cue()
                await engine.next_event(db=db, event_initiator=f"Footswitch {client_id}")
        else:
            logger.error(f"Button config not implemented: {btn_conf.action_cat}->{btn_conf.action_id}")
    
    elif category == "lights":
        # blackout
        if action == "blackout":
            engine.lights.blackout(db=db, toggle=True)
        # strobe
        elif action == "strobe":
            await manager.broadcast("Strobe not implemented!", "notification-warning")
        # blind
        elif action == "blind":
            await manager.broadcast("Blind not implemented!", "notification-warning")

        else:
            await manager.broadcast("Button not implemented!", "notification-warning")
            logger.error("Button not implemented!")

        ...
    else:
        msg = f"Button config not implemented: {btn_conf.action_cat}->{btn_conf.action_id}"
        logger.error(msg)
        await manager.broadcast(msg, "notification-warning")





@router.get('/action-types')
def get_configurable_action_types():
    return actions


@router.post('', response_model=Footswitch)
def add_new_footswitch(request: FootswitchCreate, db: Session = Depends(dependencies.get_db)):
    fs = crud.footswitch.create(db=db, obj_in=request)
    return fs

@router.post('/{fs_id}/buttons', response_model=Footswitch)
def add_button_to_footswitch(fs_id: str, db: Session = Depends(dependencies.get_db)):
    fs = crud.footswitch.get(db=db, id=fs_id)
    if not fs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No footswitch with id {fs_id} found"
        )
    nbr_of_btns = len(fs.buttons)
    # Create default btn configuration
    btn_create = _get_default_btn_conf()
    btn_create['fs_id'] = fs_id
    btn_create['btn_id'] = nbr_of_btns
    button = crud.fs_button.create(db=db, obj_in=btn_create)
    return crud.footswitch.get(id=fs_id, db=db)

@router.post('/{fs_id}/buttons/{btn_id}', response_model=Footswitch)
def update_footswitch_button(request: ButtonUpdate, fs_id: str, btn_id: int, db: Session = Depends(dependencies.get_db)):
    btn_db = crud.fs_button.get(db=db, id=btn_id)

    if not btn_db:
        raise HTTPException(
            status_code=400, detail=f"No button with id {btn_id} found"
        )
    btn = crud.fs_button.update(db=db, db_obj=btn_db, obj_in=request)
    
    return crud.footswitch.get(id=fs_id, db=db)



@router.get("", response_model=List[Footswitch])
def get_footswitches(db: Session = Depends(dependencies.get_db)):
    return crud.footswitch.get_multi(db=db)

@router.get("/{fs_id}", response_model=Footswitch)
def get_footswitch(fs_id: str, db: Session = Depends(dependencies.get_db)):
    return crud.footswitch.get(db=db, id=fs_id)


def _get_default_btn_conf()-> Button:
    btn = actions[0]
    btn['type'] = 'switch'
    btn['has_led'] = False
    return btn


@router.post("/btn-change")
async def btn_change(request: ButtonChange, db: Session = Depends(dependencies.get_db)):
    start = time.process_time()
    if request.state == 1:
        await execute(
            data=request,
            db=db,
            fs_id=request.fs_id,
            btn_id=request.btn_id
        )
    logger.info("Process time: " + str(time.process_time() - start))