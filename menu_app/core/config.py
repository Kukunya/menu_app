from os import environ

from pydantic import PostgresDsn

# POSTGRES_PORT = environ.get('POSTGRES_PORT')
# POSTGRES_HOST = environ.get('POSTGRES_HOST')
# POSTGRES_USER = environ.get('POSTGRES_USER')
# POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD')
# POSTGRES_DB = environ.get('POSTGRES_DB')
# REDIS_URI = str(environ.get('REDIS_URI'))
#
#
# SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
#     scheme='postgresql+psycopg2',
#     username=environ.get('POSTGRES_USER'),
#     password=environ.get('POSTGRES_PASSWORD'),
#     host=f'{POSTGRES_HOST}:{POSTGRES_PORT}',
#     path=environ.get('POSTGRES_DB'))

SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme='postgresql+asyncpg',
    username='postgres',
    password='admin',
    host=f'localhost',
    path='menu_app')
