
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.user import User, UserCreate
from app.models.user import User
from fastapi import APIRouter
from app import dependencies
from sqlalchemy.orm import Session
from app import crud
from typing import List
from app.device_manager import device_mgr

from  app.schemas.device import OSCDevice, OSCDeviceUpdate
router = APIRouter()


# @router.get("/mixer/search")
# def search_for_mixer():
#     """Returns the IP of the first found mixer"""
#     return engine.mixer.find_mixer()

@router.get("/", response_model=List[OSCDevice], tags=["devices"])
def get_connected_devices():
    return device_mgr.get_connected()

@router.patch("/{id}", response_model=OSCDevice, tags=["devices"])
async def device_config(id:int, request: OSCDeviceUpdate ):
    if request.ip:
        await device_mgr.set_ip(device_id=id, ip= request.ip)
    if request.receive_port:
        await device_mgr.set_receive_port(device_id=id, port=request.receive_port)
    if request.enabled is not None:
        await device_mgr.set_enabled(id, request.enabled)

