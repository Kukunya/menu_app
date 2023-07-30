from sqlalchemy import create_engine, distinct, func
from menu_app.models import Menus, Submenus, Dishes, Base
from sqlalchemy.orm import sessionmaker
from settings.conf import *
from decimal import Decimal


def create_menu(id, title, description):
    return Menus(id=id,
                 title=title,
                 description=description)


def create_submenu(id, title, description, main_menu_id):
    return Submenus(id=id,
                    title=title,
                    description=description,
                    main_menu_id=main_menu_id)


def create_dish(id, title, description, price, main_menu_id, sub_menu_id):
    return Dishes(id=id,
                  title=title,
                  description=description,
                  price=price.quantize(Decimal("1.00")),
                  main_menu_id=main_menu_id,
                  sub_menu_id=sub_menu_id)


def get_count_sbmenu_n_dsh(main_menu_id):
    return connect.query(func.count(distinct(Submenus.title)),
                         func.count(distinct(Dishes.title))).join(Dishes, isouter=True).filter(
        Submenus.main_menu_id == main_menu_id,
        Dishes.main_menu_id == main_menu_id).first()


def get_count_submenus(main_menu_id):
    return connect.query(Submenus).filter(Submenus.main_menu_id == main_menu_id).count()


def get_count_dishes(sub_menu_id):
    return connect.query(Dishes).filter(Dishes.sub_menu_id == sub_menu_id).count()


engine = create_engine(
    f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
session = sessionmaker(bind=engine)
connect = session()
Base.metadata.create_all(engine)
engine.connect()
