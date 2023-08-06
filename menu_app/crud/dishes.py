from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from menu_app.cache.crud.cache_dishes import CacheDish, dish_cache
from menu_app.crud.base import CRUDBase
from menu_app.models.dishes import Dishes
from menu_app.schemas.dish_obj import DishObj


class CRUDDishes(CRUDBase):
    def get_item(self, main_menu_id: str,
                 submenu_id: str,
                 dish_id: str,
                 db: Session) -> DishObj | None:

        cache_id = ':'.join((main_menu_id, submenu_id, dish_id))
        item = CacheDish.get_item(cache_id)
        if not item:
            item = db.query(self.model).filter(
                self.model.id == dish_id).first()

            if item:
                item = DishObj(id=dish_id,
                               title=item.title,
                               description=item.description,
                               price=item.price)
                dish_cache.add_item(data=item, id=item.id)

            else:
                return None
        return item

    def get_items(self, db: Session,
                  main_menu_id: str,
                  submenu_id: str,) -> list[DishObj]:

        return [DishObj(id=dish.id,
                        title=dish.title,
                        description=dish.description,
                        price=dish.price)
                for dish in db.query(self.model).filter(self.model.sub_menu_id == submenu_id).all()]

    def add(self, main_menu_id: str,
            submenu_id: str,
            db: Session,
            data: DishObj) -> DishObj:

        encode_data = jsonable_encoder(data)
        item = self.model(**encode_data)
        item.main_menu_id = main_menu_id
        item.sub_menu_id = submenu_id
        db.add(item)
        db.commit()
        dish_cache.update_count(main_menu_id, incr=1)
        dish_cache.update_count(submenu_id, incr=1)
        return DishObj(id=item.id,
                       title=item.title,
                       description=item.description,
                       price=item.price)

    def update(self, main_menu_id: str,
               submenu_id: str,
               dish_id: str,
               db: Session,
               data: DishObj) -> DishObj | None:

        dish = db.query(self.model).filter(self.model.id == dish_id).first()
        if dish:
            cache_id = ':'.join((main_menu_id, submenu_id, dish_id))
            dish.title = data.title
            dish.description = data.description
            dish.price = data.price
            db.commit()
            data = data.model_dump(exclude='id')
            CacheDish.update_item(id=cache_id, data=data)

            return DishObj(id=dish_id, **data)

        return None

    def delete(self, main_menu_id: str,
               submenu_id: str,
               dish_id: str,
               db: Session) -> bool:

        if db.query(self.model).filter(self.model.id == dish_id).delete():
            cache_id = ':'.join((main_menu_id, submenu_id, dish_id))
            dish_cache.delete_item(cache_id)
            dish_cache.update_count(id=main_menu_id, incr=-1)
            dish_cache.update_count(id=submenu_id, incr=-1)
            db.commit()

            return True
        return False


dishes = CRUDDishes(Dishes)
