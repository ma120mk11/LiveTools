import time
from fastapi import FastAPI, Request
from app.api.endpoints import devices, lights, songs, engine, websocket
import logging
from fastapi.middleware.cors import CORSMiddleware
import app.api.endpoints

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = FastAPI(title="LiveTools API", debug=True)

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

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(lights.router, prefix="/lights", tags=["lights"])
app.include_router(songs.router, prefix="/songs", tags=["song-book"])
app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(engine.router, prefix="/engine", tags=["engine"])
app.include_router(websocket.router, tags=["websocket"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.34.249", port=8000, log_level="debug")