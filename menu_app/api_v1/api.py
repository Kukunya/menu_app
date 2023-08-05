from fastapi import APIRouter

from menu_app.api_v1.endpoints.menus import menus

api_router = APIRouter()
api_router.include_router(menus.router)
