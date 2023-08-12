from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.api_v1 import deps
from menu_app.cache.crud.cache_menus import menu_cache
from menu_app.crud.menus import menus
from menu_app.schemas.base_obj import BaseObj
from menu_app.schemas.menu_obj import MenuObj

app = APIRouter()


@app.get('/api/v1/menus/',
         response_model=list[MenuObj])
async def get_menus(db: Session = Depends(deps.get_db)):

    return await menus.get_items(db=db)


@app.get('/api/v1/menus/{main_menu_id}/')
async def get_menu(main_menu_id: str,
                   db: Session = Depends(deps.get_db)):

    menu = await menus.get_item(main_menu_id,
                                db=db)
    if menu:
        return menu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='menu not found')


@app.post('/api/v1/menus/',
          response_model=MenuObj,
          status_code=201)
async def add_menu(data: BaseObj,
                   db: Session = Depends(deps.get_db)):

    if await menus.is_item_exist(db=db,
                                 title=data.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    menu = await menus.add(db=db,
                           data=data)
    return menu


@app.patch('/api/v1/menus/{main_menu_id}/',
           response_model=MenuObj)
async def update_menu(background_tasks: BackgroundTasks,
                      data: BaseObj,
                      main_menu_id: str,
                      db: Session = Depends(deps.get_db)):
    background_tasks.add_task(
        menu_cache.update_item, main_menu_id, data=data)

    menu = await menus.update(main_menu_id,
                              db=db,
                              data=data)
    if menu:
        return menu

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='menu not found')


@app.delete('/api/v1/menus/{main_menu_id}/',
            response_class=JSONResponse)
async def delete_menu(background_tasks: BackgroundTasks,
                      main_menu_id: str,
                      db: Session = Depends(deps.get_db)):
    background_tasks.add_task(
        menu_cache.delete_item, id=main_menu_id)

    if await menus.delete(main_menu_id,
                          db=db):
        return {'status': True,
                'message': 'The menu has been deleted'}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='menu not found')
