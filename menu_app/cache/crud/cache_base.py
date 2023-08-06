from redis.commands.json.path import Path

from menu_app.cache.cache import r


class CacheBase:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def update_item(id: str, data: dict) -> None:
        if r.exists(id):
            for k, v in data.items():
                r.json().set(id, Path(f'.{k}'), v)

    def update_count(self, id: str, incr: int) -> None:
        if r.exists(id):
            r.json().numincrby(id, Path(self.path), incr)

    @staticmethod
    def delete_item(id: str) -> None:
        match = r.scan_iter(match=f'*{id}*')
        for i in match:
            r.delete(i)
