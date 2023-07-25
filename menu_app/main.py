from fastapi import FastAPI, HTTPException, status
from typing import Union, List
from menu_app.engine import connect
from menu_app.models import Menus, Submenus, Dishes
from uuid import UUID
from menu_app.engine import create_menu, create_submenu, create_dish, count_dish, count_submenu
from menu_app.schemas import MenuObj, SubmenuObj, DishObj, RespErrNotFound, RespConfirmDel
from decimal import Decimal


app = FastAPI()


@app.get('/api/v1/menus/',
         response_model=List[MenuObj])
def get_menus():
    menus = connect.query(Menus).all()
    return [MenuObj(id=menu.id,
                    title=menu.title,
                    description=menu.description,
                    submenus_count=count_submenu(menu.id),
                    dishes_count=count_dish(menu.id)) for menu in menus]


@app.get('/api/v1/menus/{main_menu_id}/',
         response_model=MenuObj)
def get_menus_item(main_menu_id: UUID):
    menu = connect.query(Menus).filter(Menus.id == main_menu_id).first()
    if menu:
        return MenuObj(id=menu.id,
                       title=menu.title,
                       description=menu.description,
                       submenus_count=count_submenu(menu.id),
                       dishes_count=count_dish(menu.id))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found')


@app.get('/api/v1/menus/{main_menu_id}/submenus/',
         response_model=List[SubmenuObj])
def get_submenus(main_menu_id: UUID):
    sub_menus = connect.query(Submenus).filter(Submenus.main_menu_id == main_menu_id).all()
    return [SubmenuObj(id=sub_menu.id,
                       title=sub_menu.title,
                       description=sub_menu.description,
                       dishes_count=count_dish(sub_menu.id)) for sub_menu in sub_menus]


@app.get('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/',
         response_model=SubmenuObj)
def get_submenu_item(main_menu_id: UUID, sub_menu_id: UUID):
    sub_menu = connect.query(Submenus).filter(Submenus.id == sub_menu_id,
                                              Submenus.main_menu_id == main_menu_id).scalar()
    if sub_menu:
        return SubmenuObj(id=sub_menu.id,
                          title=sub_menu.title,
                          description=sub_menu.description,
                          dishes_count=count_dish(sub_menu_id=sub_menu.id))

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found')


@app.get('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/dishes/',
         response_model=List[DishObj])
def get_dishes(main_menu_id: UUID, sub_menu_id: UUID):
    dishes = connect.query(Dishes).filter(Dishes.main_menu_id == main_menu_id,
                                          Dishes.sub_menu_id == sub_menu_id).all()
    return [DishObj(id=dish.id,
                    title=dish.title,
                    description=dish.description,
                    price=dish.price) for dish in dishes]


@app.get('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}/',
         response_model=DishObj)
def get_dish_item(main_menu_id: UUID, sub_menu_id: UUID, dish_id: UUID):
    dish = connect.query(Dishes).filter(Dishes.id == dish_id).scalar()
    if dish:
        return DishObj(id=dish.id,
                       title=dish.title,
                       description=dish.description,
                       price=dish.price)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found')


@app.post('/api/v1/menus/',
          response_model=MenuObj,
          status_code=201)
def post_menu(menu: MenuObj):
    connect.add(create_menu(id=menu.id,
                            title=menu.title,
                            description=menu.description))
    connect.commit()

    return MenuObj(id=menu.id,
                   title=menu.title,
                   description=menu.description,
                   submenus_count=count_submenu(menu.id),
                   dishes_count=count_dish(menu.id))


@app.post('/api/v1/menus/{main_menu_id}/submenus/',
          response_model=MenuObj,
          status_code=201)
def post_submenu(main_menu_id: UUID, submenu: SubmenuObj):
    connect.add(create_submenu(id=submenu.id,
                               title=submenu.title,
                               description=submenu.description,
                               main_menu_id=main_menu_id))
    connect.commit()

    return MenuObj(id=submenu.id,
                   title=submenu.title,
                   description=submenu.description,
                   dishes_count=count_dish(submenu.id))


@app.post('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/dishes/',
          response_model=DishObj,
          status_code=201)
def post_dish(main_menu_id: UUID, sub_menu_id: UUID, dish: DishObj):
    connect.add(create_dish(id=dish.id,
                            title=dish.title,
                            description=dish.description,
                            price=dish.price.quantize(Decimal("1.00")),
                            main_menu_id=main_menu_id,
                            sub_menu_id=sub_menu_id))
    connect.commit()

    return DishObj(id=dish.id,
                   title=dish.title,
                   description=dish.description,
                   price=dish.price)


@app.patch('/api/v1/menus/{main_menu_id}/',
           response_model=Union[MenuObj, RespErrNotFound])
def update_menu(menu: MenuObj, main_menu_id: UUID):
    exist_menu = connect.query(Menus).filter(Menus.id == main_menu_id).scalar()
    if exist_menu:
        exist_menu.title = menu.title
        exist_menu.description = menu.description
        connect.commit()

        return MenuObj(id=exist_menu.id,
                       title=exist_menu.title,
                       description=exist_menu.description,
                       submenus_count=count_submenu(exist_menu.id),
                       dishes_count=count_dish(exist_menu.id))

    else:
        return RespErrNotFound(title='menu not found')


@app.patch('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/',
           response_model=Union[SubmenuObj, RespErrNotFound])
def update_submenu(sub_menu: MenuObj, main_menu_id: UUID, sub_menu_id: UUID):
    exist_sub_menu = connect.query(Submenus).filter(Submenus.id == sub_menu_id).scalar()
    if exist_sub_menu:
        exist_sub_menu.title = sub_menu.title
        exist_sub_menu.description = sub_menu.description
        connect.commit()

        return SubmenuObj(id=exist_sub_menu.id,
                          title=exist_sub_menu.title,
                          description=exist_sub_menu.description,
                          dishes_count=count_dish(exist_sub_menu.id))

    else:
        return RespErrNotFound(title='submenu not found')


@app.patch('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}/',
           response_model=Union[DishObj, RespErrNotFound])
def update_dish(dish: DishObj, main_menu_id: UUID, sub_menu_id: UUID, dish_id: UUID):
    exist_dish = connect.query(Dishes).filter(Dishes.id == dish_id).scalar()
    if exist_dish:
        exist_dish.title = dish.title
        exist_dish.description = dish.description
        exist_dish.price = dish.price.quantize(Decimal("1.00"))
        connect.commit()

        return DishObj(id=exist_dish.id,
                       title=exist_dish.title,
                       description=exist_dish.description,
                       price=exist_dish.price)

    else:
        return RespErrNotFound(title='dish not found')


@app.delete('/api/v1/menus/{main_menu_id}/',
            response_model=RespConfirmDel)
def delete_menu(main_menu_id: UUID):
    status = connect.query(Menus).filter(Menus.id == main_menu_id).delete()
    if status:
        connect.commit()
        return RespConfirmDel(status=True, message='The menu has been deleted')
    else:
        return RespConfirmDel(status=False, message='menu not found')


@app.delete('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/',
            response_model=RespConfirmDel)
def delete_submenu(main_menu_id: UUID, sub_menu_id: UUID):
    if connect.query(Submenus).filter(Submenus.id == sub_menu_id).delete():
        connect.commit()
        return RespConfirmDel(status=True, message='The submenu has been deleted')
    else:
        return RespConfirmDel(status=False, message='submenu not found')


@app.delete('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}/',
            response_model=RespConfirmDel)
def delete_submenu(dish_id: UUID):
    if connect.query(Dishes).filter(Dishes.id == dish_id).delete():
        connect.commit()
        return RespConfirmDel(status=True, message='The dish has been deleted')
    else:
        return RespConfirmDel(status=False, message='dish not found')
