from sqlalchemy import create_engine, distinct, func
# from menu_app.models import Menus, Submenus, Dishes, Base
from menu_app.core.config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import sessionmaker, Session
from settings.conf import *
from decimal import Decimal


engine = create_engine(str(SQLALCHEMY_DATABASE_URI))
session = sessionmaker(bind=engine)
connect = session()
engine.connect()
