"""Файл запуска приложения."""
from fastapi import FastAPI
from redis import asyncio as aioredis
import uvicorn
from config import settings
from views.crud_for_users import user_router
from views.login import login_router
from views.registration import registration_router



def get_application() -> FastAPI:
    """Возвращает экземпляр приложения.

    Returns:
        FastAPI: _description_
    """
    application = FastAPI()
    return application


application = get_application()
application.include_router(user_router)
application.include_router(login_router)
application.include_router(registration_router)

if __name__ == '__main__':
    uvicorn.run(
        app=application,
        host=settings.app_host,
        port=int(settings.app_port),
    )