from menu_app.db.session import SessionLocal
from menu_app.models.dishes import Dishes  # noqa
from menu_app.models.menus import Menus  # noqa
from menu_app.models.submenus import Submenus  # noqa


async def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
