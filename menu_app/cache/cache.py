import redis
from redis.commands.json.path import Path

from menu_app.schemas.dish_obj import DishObj
from menu_app.schemas.menu_obj import MenuObj
from menu_app.schemas.submenu_obj import SubmenuObj


def get_item(id: str) -> dict:
    if r.exists(id):
        obj_from_cache = r.json().get(id)
        return obj_from_cache
    return dict()


def update_submenu_count(id: str, incr: int) -> None:
    if r.exists(id):
        r.json().numincrby(id, Path('.submenus_count'), incr)
        update_dishes_count(id, incr)


def update_dishes_count(id: str, incr: int) -> None:
    if r.exists(id):
        r.json().numincrby(id, Path('.dishes_count'), incr)


def add_item(id: str, data: MenuObj | SubmenuObj | DishObj) -> None:
    if r.exists(id):
        r.json().set(id, '$', data.model_dump())


r = redis.Redis()
