from menu_app.db.base_class import Base
from sqlalchemy import Column, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class Submenus(Base):
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(VARCHAR, unique=True)
    description = Column(VARCHAR)
    main_menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id', ondelete='CASCADE'))