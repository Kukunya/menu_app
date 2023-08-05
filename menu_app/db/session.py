from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from menu_app.core.config import SQLALCHEMY_DATABASE_URI
from menu_app.db.base_class import Base

'''IMPORT MODELS FOR INITIALIZATION TABLES'''
from menu_app.models.dishes import Dishes  # noqa
from menu_app.models.menus import Menus  # noqa
from menu_app.models.submenus import Submenus  # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URI.unicode_string())
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
