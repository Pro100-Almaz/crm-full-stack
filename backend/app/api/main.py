from fastapi import APIRouter

from app.api.routes import branches, calendar, login, users, utils, room

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(branches.router, prefix="/branches", tags=["branches"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
api_router.include_router(room.router, prefix="/rooms", tags=["rooms"])
