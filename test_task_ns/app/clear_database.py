"""Модуль отщищения таблиц базы данных."""
import psycopg2.extras

from config import settings

DB_URL = f'postgresql://{settings.db_user}:{settings.password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'

with psycopg2.connect(DB_URL) as conn:
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM roles")
        conn.commit()
    except Exception as some_ex:
        print(some_ex)
        conn.rollback()