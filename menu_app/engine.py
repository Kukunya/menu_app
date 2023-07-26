from sqlalchemy import create_engine
from menu_app.models import session, Menus, Submenus, Dishes, Base
from sqlalchemy.orm import sessionmaker
from menu_app.conf import *
from decimal import Decimal

connect = session()


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


def get_count_submenu(main_menu_id):
    submenus_count = connect.query(Submenus).filter(Submenus.main_menu_id == main_menu_id).count()
    return submenus_count


def get_count_dish(main_menu_id=None, sub_menu_id=None):
    if main_menu_id:
        a = connect.query(Dishes).filter(Dishes.main_menu_id == main_menu_id).count()
        print(type(a))
        return connect.query(Dishes).filter(Dishes.main_menu_id == main_menu_id).count()
    elif sub_menu_id:
        return connect.query(Dishes).filter(Dishes.sub_menu_id == sub_menu_id).count()

    return connect.query(Dishes).count()


engine = create_engine(f'postgresql+psycopg2://{sql_user}:{sql_pass}@{sql_host}:{sql_port}/{sql_database}')
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
engine.connect()
