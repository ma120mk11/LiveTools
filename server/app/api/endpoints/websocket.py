
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends
from app.websocket.connection_manager import manager
from app.live_engine import engine, Engine
from app.device_manager import DeviceManager, device_mgr

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str
) -> None:

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