import os

from starlette.config import Config
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import asyncio as aioredis


dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-16]
config = Config(f'{root_dir}.env')

DB_USER = config('DB_USER', cast=str)
PASSWORD = config('PASSWORD', cast=str)
DB_HOST = config('DB_HOST', cast=str)
DB_PORT = config('DB_PORT', cast=str)
DB_NAME = config('DB_NAME', cast=str)

PATH_TO_ENV_FILE = root_dir + '.env'


class Settings(BaseSettings):
    db_user: str
    password: str
    db_host: str
    db_port: str
    db_name: str
    redis_host: str
    redis_port: str
    app_host: str
    app_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_file_encoding='utf-8')


settings = Settings(
    _env_file=PATH_TO_ENV_FILE,
    extra='ignore',
    env_file_encoding='utf-8',
)
DB_URL = f'postgresql+asyncpg://{settings.db_user}:{settings.password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
redis_instance = aioredis.from_url(
        f"redis://{settings.redis_host}:{settings.redis_port}",
        encoding="utf8",
        decode_responses=True,
)
