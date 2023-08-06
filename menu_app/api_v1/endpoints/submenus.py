from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.api_v1 import deps
from menu_app.crud.submenus import submenus
from menu_app.schemas.base_obj import BaseObj
from menu_app.schemas.submenu_obj import SubmenuObj

app = APIRouter()


@app.get('/api/v1/menus/{main_menu_id}/submenus/',
         response_model=list[SubmenuObj])
def get_submenus(main_menu_id: str,
                 db: Session = Depends(deps.get_db)):

    return submenus.get_items(db=db, main_menu_id=main_menu_id)


@app.get('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
         response_model=SubmenuObj)
def get_submenu(main_menu_id: str,
                submenu_id: str,
                db: Session = Depends(deps.get_db)):

    submenu = submenus.get_item(main_menu_id=main_menu_id,
                                submenu_id=submenu_id,
                                db=db)
    if submenu:
        return submenu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='submenu not found')


@app.post('/api/v1/menus/{main_menu_id}/submenus/',
          response_model=SubmenuObj,
          status_code=201)
def add_submenu(data: BaseObj,
                main_menu_id: str,
                db: Session = Depends(deps.get_db)):

    if submenus.is_item_exist(db=db,
                              title=data.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    submenu = submenus.add(db=db, data=data, main_menu_id=main_menu_id)
    return submenu


@app.patch('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
           response_model=SubmenuObj)
def update_submenu(data: BaseObj,
                   main_menu_id: str,
                   submenu_id: str,
                   db: Session = Depends(deps.get_db)):

    submenu = submenus.update(main_menu_id=main_menu_id,
                              submenu_id=submenu_id,
                              db=db,
                              data=data)
    if submenu:
        return submenu

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='menu not found')


@app.delete('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
            response_class=JSONResponse)
def delete_submenu(main_menu_id: str,
                   submenu_id: str,
                   db: Session = Depends(deps.get_db)):

    if submenus.delete(main_menu_id=main_menu_id,
                       submenu_id=submenu_id,
                       db=db):
        return {'status': True, 'message': 'The menu has been deleted'}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='submenu not found')
