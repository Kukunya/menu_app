from sqlalchemy import Column, VARCHAR, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Menus(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(VARCHAR, unique=True)
    description = Column(VARCHAR)


class Submenus(Base):
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(VARCHAR, unique=True)
    description = Column(VARCHAR)
    main_menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id', ondelete='CASCADE'))


class Dishes(Base):
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(VARCHAR, unique=True)
    description = Column(VARCHAR)
    price = Column(DECIMAL)
    main_menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id', ondelete='CASCADE'))
    sub_menu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id', ondelete='CASCADE'))
