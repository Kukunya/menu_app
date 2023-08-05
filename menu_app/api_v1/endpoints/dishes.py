from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from menu_app.api_v1 import deps
from menu_app.crud.dishes import dishes
from menu_app.schemas.dish_obj import DishObj

app = APIRouter()


@app.get('/api/v1/menus/{main_menu_id}/'
         'submenus/{submenu_id}/'
         'dishes/',
         response_model=List[DishObj])
def get_submenus(submenu_id: UUID,
                 db=Depends(deps.get_db)):

    return [dish for dish in dishes.get_items(db=db, id=submenu_id)]


@app.get('/api/v1/menus/{main_menu_id}/'
         'submenus/{submenu_id}/'
         'dishes/{dish_id}/',
         response_model=DishObj)
def get_submenu(dish_id: UUID,
                db=Depends(deps.get_db)):

    dish = dishes.get_item(db=db, id=dish_id)
    if dish:
        return dish

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='dish not found')


@app.post('/api/v1/menus/{main_menu_id}/'
          'submenus/{submenu_id}/dishes/',
          response_model=DishObj,
          status_code=201)
def add_submenu(data: DishObj,
                main_menu_id: UUID,
                submenu_id: UUID,
                db=Depends(deps.get_db)):

    if dishes.is_exist(db=db,
                       title=data.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    dish = dishes.add(db=db, data=data, id=[submenu_id, main_menu_id])
    return dish


@app.patch('/api/v1/menus/{main_menu_id}/'
           'submenus/{submenu_id}/'
           'dishes/{dish_id}/',
           response_model=DishObj)
def update_submenu(data: DishObj,
                   dish_id: UUID,
                   db=Depends(deps.get_db)):

    dish = dishes.update(db, data, dish_id)
    if dish:
        return dish

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='dish not found')


@app.delete('/api/v1/menus/{main_menu_id}/'
            'submenus/{sub_menu_id}/'
            'dishes/{dish_id}/',
            response_class=JSONResponse)
def delete_submenu(dish_id: UUID,
                   db=Depends(deps.get_db)):

    if dishes.delete(db=db, id=dish_id):
        return {"status": True, "message": "The menu has been deleted"}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='dish not found')
