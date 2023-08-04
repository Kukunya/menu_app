from pydantic import PostgresDsn
from os import environ


POSTGRES_PORT = environ.get('POSTGRES_PORT')
POSTGRES_HOST = environ.get('POSTGRES_HOST')
POSTGRES_USER = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = environ.get('POSTGRES_DB')


# SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
#     scheme="postgresql+psycopg2",
#     username=environ.get('POSTGRES_USER'),
#     password=environ.get('POSTGRES_PASSWORD'),
#     host=f"localhost:5432",
#     path=environ.get('POSTGRES_DB'),
# )

SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql+psycopg2",
    username="postgres",
    password="admin",
    host=f"localhost:5432",
    path="menu_app",)
