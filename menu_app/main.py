from fastapi import FastAPI

from menu_app.api_v1.endpoints import dishes, menus, submenus

app = FastAPI()

app.include_router(menus.app)
app.include_router(submenus.app)
app.include_router(dishes.app)
