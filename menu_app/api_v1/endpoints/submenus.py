from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from menu_app.api_v1 import deps
from menu_app.crud.submenus import submenus
from menu_app.schemas.submenu_obj import SubmenuObj

app = APIRouter()


@app.get('/api/v1/menus/{main_menu_id}/submenus/',
         response_model=list[SubmenuObj])
def get_submenus(main_menu_id: UUID,
                 db=Depends(deps.get_db)):

    return [SubmenuObj(id=submenu.id,
                       title=submenu.title,
                       description=submenu.description)
            for submenu in submenus.get_items(db=db, id=main_menu_id)]


@app.get('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
         response_model=SubmenuObj)
def get_submenu(submenu_id: UUID,
                db=Depends(deps.get_db)):

    submenu = submenus.get_item(db=db, id=submenu_id)
    if submenu:
        return SubmenuObj(id=submenu.id,
                          title=submenu.title,
                          description=submenu.description)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='submenu not found')


@app.post('/api/v1/menus/{main_menu_id}/submenus/',
          response_model=SubmenuObj,
          status_code=201)
def add_submenu(data: SubmenuObj,
                main_menu_id: UUID,
                db=Depends(deps.get_db)):

    if submenus.is_exist(db=db,
                         title=data.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    submenu = submenus.add(db=db, data=data, id=main_menu_id)
    return SubmenuObj(id=submenu.id,
                      title=submenu.title,
                      description=submenu.description)


@app.patch('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
           response_model=SubmenuObj)
def update_submenu(data: SubmenuObj,
                   submenu_id: UUID,
                   db=Depends(deps.get_db)):

    submenu = submenus.update(db, data, submenu_id)
    if submenu:
        return SubmenuObj(id=submenu.id,
                          title=submenu.title,
                          description=submenu.description)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='submenu not found')


@app.delete('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
            response_class=JSONResponse)
def delete_submenu(submenu_id: UUID,
                   db=Depends(deps.get_db)):
    if submenus.delete(db=db, id=submenu_id):
        return {'status': True, 'message': 'The menu has been deleted'}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='submenu not found')
