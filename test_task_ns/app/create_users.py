"""Модуль создания пользователей."""
import psycopg2.extras

from config import settings
from data_sources.storages.user_repository import get_password_hash

DB_URL = f'postgresql://{settings.db_user}:{settings.password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

with psycopg2.connect(DB_URL) as conn:
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users(id, name, surname, email, password, role) VALUES(%s, %s, %s, %s, %s, %s)",
            (
                1,
                'Федер',
                'Михайлов',
                'email1@mail.ru',
                get_password_hash('password'),
                1,
            )
        )
        cursor.execute(
            "INSERT INTO users(id, name, surname, email, password, role) VALUES(%s, %s, %s, %s, %s, %s)",
            (
                2,
                'Олег',
                'Петров',
                'email2@mail.ru',
                get_password_hash('password2'),
                2,
            )
        )
        conn.commit()
    except Exception as some_ex:
        print(some_ex)
        conn.rollback()