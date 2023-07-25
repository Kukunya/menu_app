from sqlalchemy import create_engine
from menu_app.models import session, Menus, Submenus, Dishes, Base
from sqlalchemy.orm import sessionmaker

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
                  price=price,
                  main_menu_id=main_menu_id,
                  sub_menu_id=sub_menu_id)


def count_submenu(main_menu_id):
    submenus_count = connect.query(Submenus).filter(Submenus.main_menu_id == main_menu_id).count()
    return submenus_count


def count_dish(main_menu_id=None, sub_menu_id=None):
    if main_menu_id:
        a = connect.query(Dishes).filter(Dishes.main_menu_id == main_menu_id).count()
        print(type(a))
        return connect.query(Dishes).filter(Dishes.main_menu_id == main_menu_id).count()
    elif sub_menu_id:
        return connect.query(Dishes).filter(Dishes.sub_menu_id == sub_menu_id).count()

    return connect.query(Dishes).count()


engine = create_engine(f'postgresql+psycopg2://postgres:admin@localhost:5432/menu_app')
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
engine.connect()
