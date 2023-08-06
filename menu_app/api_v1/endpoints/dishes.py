from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from menu_app.api_v1 import deps
from menu_app.crud.dishes import dishes
from menu_app.schemas.dish_obj import DishObj

app = APIRouter()


@app.get('/api/v1/menus/{main_menu_id}/'
         'submenus/{submenu_id}/'
         'dishes/',
         response_model=list[DishObj])
def get_dishes(main_menu_id: str,
               submenu_id: str,
               db: Session = Depends(deps.get_db)):

    return dishes.get_items(db=db,
                            main_menu_id=main_menu_id,
                            submenu_id=submenu_id)


@app.get('/api/v1/menus/{main_menu_id}/'
         'submenus/{submenu_id}/'
         'dishes/{dish_id}/',
         response_model=DishObj)
def get_dish(main_menu_id: str,
             submenu_id: str,
             dish_id: str,
             db: Session = Depends(deps.get_db)):

    dish = dishes.get_item(main_menu_id=main_menu_id,
                           submenu_id=submenu_id,
                           dish_id=dish_id,
                           db=db)
    if dish:
        return dish

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='dish not found')


@app.post('/api/v1/menus/{main_menu_id}/'
          'submenus/{submenu_id}/'
          'dishes/',
          response_model=DishObj,
          status_code=201)
def add_dish(data: DishObj,
             main_menu_id: str,
             submenu_id: str,
             db: Session = Depends(deps.get_db)):

    if dishes.is_item_exist(db=db,
                            title=data.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    dish = dishes.add(main_menu_id=main_menu_id,
                      submenu_id=submenu_id,
                      db=db,
                      data=data)
    return dish


@app.patch('/api/v1/menus/{main_menu_id}/'
           'submenus/{submenu_id}/'
           'dishes/{dish_id}/',
           response_model=DishObj)
def update_dish(data: DishObj,
                main_menu_id: str,
                submenu_id: str,
                dish_id: str,
                db: Session = Depends(deps.get_db)):

    dish = dishes.update(main_menu_id=main_menu_id,
                         submenu_id=submenu_id,
                         dish_id=dish_id,
                         db=db,
                         data=data)
    if dish:
        return dish

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='dish not found')


@app.delete('/api/v1/menus/{main_menu_id}/'
            'submenus/{submenu_id}/'
            'dishes/{dish_id}/',
            response_class=JSONResponse)
def delete_dish(main_menu_id: str,
                submenu_id: str,
                dish_id: str,
                db: Session = Depends(deps.get_db)):

    if dishes.delete(main_menu_id=main_menu_id,
                     submenu_id=submenu_id,
                     dish_id=dish_id,
                     db=db):
        return {'status': True, 'message': 'The menu has been deleted'}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='dish not found')
