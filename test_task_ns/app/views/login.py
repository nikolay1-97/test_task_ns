"""Модуль с логикой аутентификации пользователей."""
import datetime

from fastapi import APIRouter, Depends
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status

from data_sources.models import get_async_session
from pydantic_models.pydantic_models import LoginModel
from data_sources.storages.token_reposytory import TokenRepository
from data_sources.storages.user_repository import (
    authenticate_user,
    create_access_token,
)
from config import settings

login_router = APIRouter()

@login_router.post('/api/v1/login')
async def login(
    request: LoginModel,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на авторизацию пользователя.

        Parameters
        ----------
        request: LoginModel
            Модель данных запроса.
        response: Response
            Объект Response.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
    #Текущий пользователь.
    user = await authenticate_user(
        request.email,
        request.password,
        session,
    )
    if not user:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Неверный логин или пароль',
            )
    access_token_expires = datetime.timedelta(
        minutes=int(settings.access_token_expire_minutes),
    )
    token = create_access_token(
        data={"sub": request.email},
        expires_delta=access_token_expires,
    )
    await TokenRepository.write_token(user[0][3], token)
    response.set_cookie(key='email', value=str(user[0][3]))
    return {"message": "Пользователь успешно авторизован", 'user_id': user[0][0]}