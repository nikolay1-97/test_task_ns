"""Хендлер регистрации нового пользователя."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data_sources.models import get_async_session
from pydantic_models.pydantic_models import RegistrationModel
from data_sources.storages.user_repository import UserRepository

registration_router = APIRouter()


@registration_router.post('/api/v1/users_registration')
async def registration_user(
    request: RegistrationModel,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на регистрацию нового пользователя.

        Parameters
        ----------
        request: RegistrationModel
            Модель данных запроса.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
    return await UserRepository.registration_user(
        request.name,
        request.surname,
        request.email,
        request.password,
        session,
    )