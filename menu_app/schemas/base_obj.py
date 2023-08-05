from uuid import UUID, uuid4

from pydantic import BaseModel


class BaseObj(BaseModel):
    id: str | UUID | None = None
    title: str
    description: str

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid4())
        super().__init__(**data)
