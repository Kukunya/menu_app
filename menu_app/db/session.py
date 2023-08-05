from sqlalchemy import create_engine
from menu_app.core.config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import sessionmaker
from menu_app.db.base_class import Base
from menu_app.models.menus import Menus
from menu_app.models.submenus import Submenus
from menu_app.models.dishes import Dishes


engine = create_engine(str(SQLALCHEMY_DATABASE_URI))
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)