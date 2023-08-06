from uuid import UUID

from menu_app.cache.cache import r
from menu_app.cache.crud.cache_base import CacheBase
from menu_app.schemas.dish_obj import DishObj


class CacheDish(CacheBase):
    @staticmethod
    def get_item(id: str) -> DishObj | None:
        obj_from_cache = r.json().get(id)
        if obj_from_cache:
            return DishObj(**obj_from_cache)
        return None

    @staticmethod
    def add_item(id: str | UUID | None, data: DishObj) -> None:
        data = data.model_dump()
        data['price'] = str(data['price'])
        r.json().set(id, '$', data)


dish_cache = CacheDish('.dishes_count')
