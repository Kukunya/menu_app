
@app.get('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/dishes/',
         response_model=List[DishObj])
def get_dishes(main_menu_id: UUID,
               submenu_id: UUID):
    dishes = connect.query(Dishes).filter(Dishes.main_menu_id == main_menu_id,
                                          Dishes.sub_menu_id == submenu_id).all()

    return [DishObj(id=dish.id,
                    title=dish.title,
                    description=dish.description,
                    price=dish.price) for dish in dishes]


@app.get('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/dishes/{dish_id}/',
         response_model=DishObj)
def get_dish_item(dish_id: UUID):
    dish = connect.query(Dishes).filter(Dishes.id == dish_id).scalar()
    if dish:
        return DishObj(id=dish.id,
                       title=dish.title,
                       description=dish.description,
                       price=dish.price)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='dish not found')

@app.post('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/dishes/',
          response_model=DishObj,
          status_code=201)
def add_dish(main_menu_id: UUID,
             submenu_id: UUID,
             dish: DishObj):
    if connect.query(Dishes).filter(Dishes.title == dish.title).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    if not connect.query(Submenus).filter(Submenus.id == submenu_id).scalar():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='there is no parent menu')

    connect.add(create_dish(id=dish.id,
                            title=dish.title,
                            description=dish.description,
                            price=dish.price,
                            main_menu_id=main_menu_id,
                            sub_menu_id=submenu_id))
    connect.commit()
    return DishObj(id=dish.id,
                   title=dish.title,
                   description=dish.description,
                   price=dish.price)

@app.patch('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/dishes/{dish_id}/',
           response_model=DishObj)
def update_dish(dish: DishObj,
                dish_id: UUID):
    exist_dish = connect.query(Dishes).filter(Dishes.id == dish_id).scalar()
    if exist_dish:
        exist_dish.title = dish.title
        exist_dish.description = dish.description
        exist_dish.price = dish.price
        connect.commit()

        return DishObj(id=exist_dish.id,
                       title=exist_dish.title,
                       description=exist_dish.description,
                       price=exist_dish.price)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='dish not found')

@app.delete('/api/v1/menus/{main_menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}/',
            response_class=JSONResponse)
def delete_submenu(dish_id: UUID):
    if connect.query(Dishes).filter(Dishes.id == dish_id).delete():
        connect.commit()
        return {"status": True, "message": "The menu has been deleted"}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='dish not found')