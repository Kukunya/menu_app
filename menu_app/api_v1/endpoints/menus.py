from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from menu_app.api_v1 import deps
from menu_app.crud.menus import menus
from menu_app.schemas.menu_obj import MenuObj

app = APIRouter()


@app.get('/api/v1/menus/',
         response_model=list[MenuObj])
def get_menus(db=Depends(deps.get_db)):

    return [MenuObj(id=menu.id,
                    title=menu.title,
                    description=menu.description)
            for menu in menus.get_items(db=db)]


@app.get('/api/v1/menus/{main_menu_id}/',
         response_model=MenuObj)
def get_menu(main_menu_id: UUID,
             db=Depends(deps.get_db)):

    menu = menus.get_item(db=db, id=main_menu_id)
    if menu:
        return MenuObj(id=menu.id,
                       title=menu.title,
                       description=menu.description)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='menu not found')


@app.post('/api/v1/menus/',
          response_model=MenuObj,
          status_code=201)
def add_menu(data: MenuObj,
             db=Depends(deps.get_db)):

    if menus.is_exist(db=db, title=data.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    menu = menus.add(db=db, data=data)
    return MenuObj(id=menu.id,
                   title=menu.title,
                   description=menu.description)


@app.patch('/api/v1/menus/{main_menu_id}/',
           response_model=MenuObj)
def update_menu(data: MenuObj,
                main_menu_id: UUID,
                db=Depends(deps.get_db)):
    menu = menus.update(db, data, main_menu_id)
    if menu:
        return MenuObj(id=menu.id,
                       title=menu.title,
                       description=menu.description)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='menu not found')


@app.delete('/api/v1/menus/{main_menu_id}/',
            response_class=JSONResponse)
def delete_menu(main_menu_id: UUID,
                db=Depends(deps.get_db)):
    if menus.delete(db=db, id=main_menu_id):
        return {'status': True, 'message': 'The menu has been deleted'}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='menu not found')
