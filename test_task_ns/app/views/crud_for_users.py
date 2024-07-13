"""Хендлеры для сущности пользователь."""
from fastapi import APIRouter, Depends
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette import status

from data_sources.models import get_async_session
from pydantic_models.pydantic_models import UserModel, UserUpdate
from data_sources.storages.user_repository import UserRepository, verify_token
from data_sources.storages.role_repository import RoleRepository
from data_sources.storages.token_reposytory import TokenRepository

user_router = APIRouter()

@user_router.post('/api/v1/users')
async def create_user(
    req: Request,
    request: UserModel,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на создание нового пользователя.

        Parameters
        ----------
        req: Request
            Объект Request.
        requests: UserModel
            Модель данных запроса.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
    #Email текущего пользователя.
    email = req.cookies.get('email')

    #Текущий пользователь.
    user = await UserRepository.get_user_by_email(email, session)

    #Роль текущего пользователя.
    role = await RoleRepository.get_role_by_id(user[0][5], session)
    token = await TokenRepository.get_token(email)
    if not verify_token(token):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Время действия токена истекло',
            )
    
    if role[0][1] != 'admin':
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Доступ ограничен',
            )

    return await UserRepository.create_user(
        request.name,
        request.surname,
        request.email,
        request.password,
        request.role,
        session,
    )


@user_router.post('/api/v1/users/{user_id}')
async def update_user(
    req: Request,
    request: UserUpdate,
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на обновление данных пользователя.

        Parameters
        ----------
        req: Request
            Объект Request.
        requests: UserUpdate
            Модель данных запроса.
        user_id: str
            id пользователя.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
    #Email текущего пользователя.
    email = req.cookies.get('email')

    #Текущий пользователь.
    user = await UserRepository.get_user_by_email(email, session)

    # Роль текущего пользователя.
    role = await RoleRepository.get_role_by_id(user[0][5], session)
    token = await TokenRepository.get_token(email)
    if not verify_token(token):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Время действия токена истекло',
            )
    
    if role[0][1] != 'admin':
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Доступ ограничен',
            )

    return await UserRepository.update_user(
        request.name,
        request.surname,
        request.email,
        request.role,
        user_id,
        session,
    )

@user_router.get('/api/v1/users')
async def get_users_list(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на получение списка пользователей.

        Parameters
        ----------
        requests: Request
            Объект Request.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
    #Email текущего пользователя.
    email = request.cookies.get('email')

    #Текущий пользователь.
    user = await UserRepository.get_user_by_email(email, session)

    #Роль текущего пользователя.
    role = await RoleRepository.get_role_by_id(user[0][5], session)
    token = await TokenRepository.get_token(email)
    if not verify_token(token):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Время действия токена истекло',
            )
    
    if role[0][1] != 'admin':
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Доступ ограничен',
            )

    return await UserRepository.get_users_list(session)


@user_router.delete('/api/v1/users/{user_id}')
async def delete_user(
    request: Request,
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Запрос на удаление пользователя.

        Parameters
        ----------
        requests: Request
            Объект Request.
        user_id: str
            id пользователя
        session: AsyncSession
            Сессия соединения с базой данных.
        """
    #Email текущего пользователя.
    email = request.cookies.get('email')

    #Текущий пользователь.
    user = await UserRepository.get_user_by_email(email, session)

    #Роль текущего пользователя.
    role = await RoleRepository.get_role_by_id(user[0][5], session)
    token = await TokenRepository.get_token(email)
    if not verify_token(token):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Время действия токена истекло',
            )
    
    if role[0][1] != 'admin':
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Доступ ограничен',
            )

    return await UserRepository.delete_user(user_id, session)