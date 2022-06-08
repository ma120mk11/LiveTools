from fastapi import APIRouter

from app.api.endpoints import lights


api_router = APIRouter()
# api_router.include_router(lights.router, prefix="/lights", tags=["lights"])

# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])