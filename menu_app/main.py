from fastapi import FastAPI
from menu_app.api_v1.endpoints import menus
from menu_app.api_v1.endpoints import submenus
from menu_app.api_v1.endpoints import dishes

app = FastAPI()

app.include_router(menus.app)
app.include_router(submenus.app)
app.include_router(dishes.app)


