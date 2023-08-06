from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from menu_app.cache.crud.cache_submenus import CacheSubmenu, submenu_cache
from menu_app.crud.base import CRUDBase
from menu_app.models.submenus import Submenus
from menu_app.schemas.base_obj import BaseObj
from menu_app.schemas.submenu_obj import SubmenuObj


class CRUDSubmenus(CRUDBase):
    def get_item(self, main_menu_id: str,
                 submenu_id: str,
                 db: Session) -> SubmenuObj | None:

        cache_id = ':'.join((main_menu_id, submenu_id))

        item = CacheSubmenu.get_item(cache_id)
        if not item:
            item = db.query(self.model).filter(
                self.model.id == submenu_id).first()

            if item:
                item = SubmenuObj(id=submenu_id,
                                  title=item.title,
                                  description=item.description)
                CacheSubmenu.add_item(data=item, id=cache_id)

            else:
                return None
        return item

    def get_items(self, db: Session,
                  main_menu_id: str) -> list[SubmenuObj]:

        return [SubmenuObj(id=submenu.id,
                           title=submenu.title,
                           description=submenu.description)
                for submenu in db.query(self.model).filter(
                self.model.main_menu_id == main_menu_id).all()]

    def add(self, db: Session,
            data: BaseObj,
            main_menu_id: str) -> SubmenuObj:
        encode_data = jsonable_encoder(data,
                                       exclude={'dishes_count'})
        item = self.model(**encode_data)
        item.main_menu_id = main_menu_id
        db.add(item)
        db.commit()
        submenu_cache.update_submenu_count(id=main_menu_id, incr=1)

        return SubmenuObj(**encode_data)

    def update(self, submenu_id: str,
               main_menu_id: str,
               db: Session,
               data: BaseObj) -> SubmenuObj | None:

        cache_id = ':'.join((main_menu_id, submenu_id))
        submenu = db.query(self.model).filter(self.model.id == submenu_id).first()
        if submenu:
            submenu.title = data.title
            submenu.description = data.description
            db.commit()
            data = data.model_dump(exclude='id')
            CacheSubmenu.update_item(id=cache_id, data=data)

            return SubmenuObj(id=submenu_id, **data)

        return None

    def delete(self, main_menu_id: str,
               submenu_id: str,
               db: Session) -> bool:

        cache_id = ':'.join((main_menu_id, submenu_id))
        submenu_cache.delete_item(cache_id)
        submenu_cache.update_submenu_count(id=main_menu_id, incr=-1)

        if db.query(self.model).filter(self.model.id == submenu_id).delete():
            db.commit()

            return True
        return False


submenus = CRUDSubmenus(Submenus)
