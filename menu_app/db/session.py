from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from menu_app.core.config import SQLALCHEMY_DATABASE_URI

'''IMPORT MODELS FOR INITIALIZATION TABLES'''
# from menu_app.models.dishes import Dishes  # noqa
# from menu_app.models.menus import Menus  # noqa
# from menu_app.models.submenus import Submenus  # noqa

engine = create_async_engine(SQLALCHEMY_DATABASE_URI.unicode_string())
SessionLocal = async_sessionmaker(engine)
