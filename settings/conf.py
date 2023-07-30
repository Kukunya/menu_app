from os import environ


POSTGRES_PORT = environ.get('POSTGRES_PORT')
POSTGRES_HOST = environ.get('POSTGRES_HOST')
POSTGRES_USER = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = environ.get('POSTGRES_DB')
