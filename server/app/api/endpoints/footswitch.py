
from http.client import HTTPException
import json
import logging
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import APIRouter, Depends
from app.websocket.connection_manager import manager
from app.live_engine import engine
from app.schemas.footswitch import Footswitch, FootswitchCreate, ButtonCreate, Button, ButtonUpdate
from app.models.footswitch import Button as ButtonModel, Footswitch as FootswitchModel
from app import crud, dependencies
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter()


actions = [
    {"name": "Next", "action_cat": "engine", "action_id": "next"},
    {"name": "Blackout", "action_cat": "light_cmd", "action_id": "blackout"},
    {"name": "Strobe", "action_cat": "light_cmd", "action_id": "strobe"},
    {"name": "Blind", "action_cat": "light_cmd", "action_id": "blind"},
    {"name": "Add speech", "action_cat": "engine", "action_id": "speech-add"},
    {"name": "Speech", "action_cat": "engine", "action_id": "speech-next"},
    {"name": "Song btn 1", "action_cat": "song", "action_id": "btn-1"},
    {"name": "Song btn 2", "action_cat": "song", "action_id": "btn-2"},
]

@router.websocket("/{client_id}")
async def websocket_footswitch(
    websocket: WebSocket,
    client_id: str,
    db: Session = Depends(dependencies.get_db)
) -> None:

    await connect(websocket, client_id)

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Footswitch {client_id}: {data}")

            data = json.loads(data)

            if (data['type'] == "btn-change") and (data['data']['state'] == 1):
                btn_conf = {}
                btn_id = data['data']['button_id']

                btn_conf = db.query(ButtonModel).filter(ButtonModel.id == btn_id).first()

                if not btn_conf:
                    logger.error("Button config not found")

                # Button actions ///////////////////////////////////////////////////
                category = btn_conf.action_cat
                action = btn_conf.action_id
                # engine
                if category == "engine":
                    # next
                    if action == "next":
                        await engine.next_event(f"Footswitch {client_id}")
                    # blackout
                    elif action == "blackout":
                        engine.lights.blackout()
                    # Speech
                    elif action == "speech-add":
                            await engine.add_speech_to_cue()
                    # Speech
                    elif action == "speech-next":
                            await engine.add_speech_to_cue()
                            await engine.next_event()
                    else:
                        logger.error(f"Button config not implemented: {btn_conf.action_cat}->{btn_conf.action_id}")
                
                elif category == "light_cmd":
                    ...
                else:
                    msg = f"Button config not implemented: {btn_conf.action_cat}->{btn_conf.action_id}"
                    logger.error(msg)
                    await manager.broadcast(msg, "notification-warning")


    except WebSocketDisconnect:
        # Notify web clients
        await manager.broadcast(f"Footswitch {client_id} disconnected", "notification")



async def connect(websocket: WebSocket, client_id: str):
    await websocket.accept()
    logger.info("Footswitch client connected: %s", client_id)




@router.get('/action-types')
def get_configurable_action_types():
    return actions


@router.post('', response_model=Footswitch)
def add_new_footswitch(request: FootswitchCreate, db: Session = Depends(dependencies.get_db)):
    fs = crud.footswitch.create(db=db, obj_in=request)
    return fs

@router.post('/{fs_id}/buttons', response_model=Footswitch)
def add_button_to_footswitch(fs_id: str, db: Session = Depends(dependencies.get_db)):

    # Create default btn configuration
    btn_create = _get_default_btn_conf()
    btn_create['fs_id'] = fs_id
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

