from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.api_v1 import deps
from menu_app.cache.crud.cache_submenus import submenu_cache
from menu_app.crud.submenus import submenus
from menu_app.schemas.base_obj import BaseObj
from menu_app.schemas.submenu_obj import SubmenuObj

app = APIRouter()


@app.get('/api/v1/menus/{main_menu_id}/submenus/',
         response_model=list[SubmenuObj])
async def get_submenus(main_menu_id: str,
                       db: Session = Depends(deps.get_db)):

    return await submenus.get_items(db=db,
                                    top_id=main_menu_id)


@app.get('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/')
async def get_submenu(main_menu_id: str,
                      submenu_id: str,
                      db: Session = Depends(deps.get_db)):

    submenu = await submenus.get_item(main_menu_id,
                                      submenu_id,
                                      db=db)
    if submenu:
        return submenu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='submenu not found')


@app.post('/api/v1/menus/{main_menu_id}/submenus/',
          response_model=SubmenuObj,
          status_code=201)
async def add_submenu(data: BaseObj,
                      main_menu_id: str,
                      db: Session = Depends(deps.get_db)):

    if await submenus.is_item_exist(db=db,
                                    title=data.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    submenu = await submenus.add(main_menu_id=main_menu_id,
                                 db=db,
                                 data=data)
    return submenu


@app.patch('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
           response_model=SubmenuObj)
async def update_submenu(background_tasks: BackgroundTasks,
                         data: BaseObj,
                         main_menu_id: str,
                         submenu_id: str,
                         db: Session = Depends(deps.get_db)):
    background_tasks.add_task(
        submenu_cache.update_item, main_menu_id, submenu_id, data=data)

    submenu = await submenus.update(main_menu_id,
                                    submenu_id,
                                    db=db,
                                    data=data)
    if submenu:
        return submenu

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='menu not found')


@app.delete('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
            response_class=JSONResponse)
async def delete_submenu(background_tasks: BackgroundTasks,
                         main_menu_id: str,
                         submenu_id: str,
                         db: Session = Depends(deps.get_db)):
    background_tasks.add_task(
        submenu_cache.delete_item, id=submenu_id)

    if await submenus.delete(main_menu_id,
                             submenu_id,
                             db=db):
        return {'status': True, 'message': 'The menu has been deleted'}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='submenu not found')
