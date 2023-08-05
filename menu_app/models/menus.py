from sqlalchemy import VARCHAR, Column
from sqlalchemy.dialects.postgresql import UUID

from menu_app.db.base_class import Base


class Menus(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(VARCHAR, unique=True)
    description = Column(VARCHAR)
