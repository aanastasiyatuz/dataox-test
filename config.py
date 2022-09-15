import peewee
from decouple import config

pg_database = peewee.PostgresqlDatabase(
        database=config("DB_NAME"),
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),
        host=config("DB_HOST"),
        port=5432
    )