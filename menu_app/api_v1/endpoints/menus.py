from typing import List
from fastapi import APIRouter, Depends, HTTPException
from menu_app import schemas
from menu_app.api_v1 import deps
from menu_app.crud.menus import menus
from fastapi import status


app = APIRouter()


@app.get('/api/v1/menus/',
         response_model=List[schemas.MenuObj])
def get_menus(db=Depends(deps.get_db())):
    return [menu for menu in menus.get_items(db=db)]


@app.get('/api/v1/menus/{main_menu_id}/',
         response_model=schemas.MenuObj)
def get_menus_item(main_menu_id: UUID,
                   db=Depends(deps.get_db())):

    menu = menus.get_item(db=db, id=main_menu_id)
    if menu:
        count_submenu, count_dish = get_count_sbmenu_n_dsh(main_menu_id)
        return schemas.MenuObj(id=menu.id,
                               title=menu.title,
                               description=menu.description,
                               submenus_count=count_submenu,
                               dishes_count=count_dish)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='menu not found')


@app.post('/api/v1/menus/',
          response_model=schemas.MenuObj,
          status_code=201)
def add_menu(db=Depends(deps.get_db()),
             menu: schemas.MenuObj):
    if connect.query(Menus).filter(Menus.title == Menus.title).scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    connect.add(create_menu(id=menu.id,
                            title=menu.title,
                            description=menu.description))
    connect.commit()
    return schemas.MenuObj(id=menu.id,
                   title=menu.title,
                   description=menu.description,
                   submenus_count=get_count_submenus(menu.id),
                   dishes_count=get_count_dishes(menu.id))


@app.patch('/api/v1/menus/{main_menu_id}/',
           response_model=schemas.MenuObj)
def update_menu(db=Depends(deps.get_db()),
                menu: schemas.MenuObj,
                main_menu_id: UUID):
    exist_menu = connect.query(Menus).filter(Menus.id == main_menu_id).scalar()
    if exist_menu:
        exist_menu.title = menu.title
        exist_menu.description = menu.description
        connect.commit()

        return schemas.MenuObj(id=exist_menu.id,
                       title=exist_menu.title,
                       description=exist_menu.description,
                       submenus_count=get_count_submenus(exist_menu.id),
                       dishes_count=get_count_dishes(exist_menu.id))

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='menu not found')


@app.delete('/api/v1/menus/{main_menu_id}/',
            response_class=JSONResponse)
def delete_menu(db=Depends(deps.get_db()),
                main_menu_id: UUID):
    if connect.query(Menus).filter(Menus.id == main_menu_id).delete():
        connect.commit()
        return {"status": True, "message": "The menu has been deleted"}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='menu not found')