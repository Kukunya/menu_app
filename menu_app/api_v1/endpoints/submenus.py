@app.get('/api/v1/menus/{main_menu_id}/submenus/',
         response_model=List[SubmenuObj])
def get_submenus(main_menu_id: UUID):
    sub_menus = connect.query(Submenus).filter(
        Submenus.main_menu_id == main_menu_id).all()
    return [SubmenuObj(id=sub_menu.id,
                       title=sub_menu.title,
                       description=sub_menu.description,
                       dishes_count=get_count_dishes(sub_menu.id)) for sub_menu in sub_menus]


@app.get('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
         response_model=SubmenuObj)
def get_submenu_item(main_menu_id: UUID,
                     submenu_id: UUID):
    sub_menu = connect.query(Submenus).filter(Submenus.id == submenu_id,
                                              Submenus.main_menu_id == main_menu_id).scalar()
    if sub_menu:
        return SubmenuObj(id=sub_menu.id,
                          title=sub_menu.title,
                          description=sub_menu.description,
                          dishes_count=get_count_dishes(sub_menu_id=submenu_id))

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='submenu not found')


@app.post('/api/v1/menus/{main_menu_id}/submenus/',
          response_model=SubmenuObj,
          status_code=201)
def add_submenu(main_menu_id: UUID,
                submenu: SubmenuObj):
    if connect.query(Submenus).filter(Submenus.title == submenu.title).scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='such a item already exists')

    if not connect.query(Menus).filter(Menus.id == main_menu_id).scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='there is no parent menu')


@app.patch('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
           response_model=SubmenuObj)
def update_submenu(sub_menu: MenuObj,
                   submenu_id: UUID):
    exist_sub_menu = connect.query(Submenus).filter(
        Submenus.id == submenu_id).scalar()
    if exist_sub_menu:
        exist_sub_menu.title = sub_menu.title
        exist_sub_menu.description = sub_menu.description
        connect.commit()

        return SubmenuObj(id=exist_sub_menu.id,
                          title=exist_sub_menu.title,
                          description=exist_sub_menu.description,
                          dishes_count=get_count_dishes(exist_sub_menu.id))

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='submenu not found')

@app.delete('/api/v1/menus/{main_menu_id}/submenus/{submenu_id}/',
            response_class=JSONResponse)
def delete_submenu(submenu_id: UUID):
    if connect.query(Submenus).filter(Submenus.id == submenu_id).delete():
        connect.commit()
        return {"status": True, "message": "The menu has been deleted"}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='submenu not found')