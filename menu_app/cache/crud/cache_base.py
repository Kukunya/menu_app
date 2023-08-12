from redis.commands.json.path import Path

from menu_app.cache.cache import r
from menu_app.schemas.base_obj import BaseObj
from menu_app.schemas.dish_obj import DishObj
from menu_app.schemas.menu_obj import MenuObj
from menu_app.schemas.submenu_obj import SubmenuObj


class CacheBase:
    def __init__(self, path):
        self.path = path

    @staticmethod
    async def get_item(id: str):
        cache_id = ':'.join(id)
        obj_from_cache = await r.json().get(cache_id)

        if obj_from_cache:
            return obj_from_cache
        return None

    @staticmethod
    async def add_item(id: str,
                       data: MenuObj | DishObj | SubmenuObj) -> None:
        cache_id = ':'.join(id)
        await r.json().set(cache_id, '$', data.model_dump(mode='json'))

    @staticmethod
    async def update_item(*id: str, data: BaseObj | DishObj) -> None:
        cache_id = ':'.join(id)
        if await r.exists(cache_id):
            item = data.model_dump(exclude='id', mode='json')
            for k, v in item.items():
                await r.json().set(cache_id, Path(f'.{k}'), v)

    async def update_count(self, id: str, incr: int) -> None:
        if r.exists(id):
            await r.json().numincrby(id, Path(self.path), incr)

    @staticmethod
    async def delete_item(id: str) -> None:
        match = r.scan_iter(match=f'*{id}*')
        async for i in match:
            await r.delete(i)
