"""Операции с данными для сущности меню и вспомогательные функции."""
import datetime
import hashlib

from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from pydantic_models.pydantic_models import UserModelResp, UserUpdateResp
from data_sources.models import Users_model
from data_sources.storages.role_repository import RoleRepository
from config import settings

def get_password_hash(password: str):
    """Возвращает хеш пароля.

        Parameters
        ----------
        password: str
            Пароль.
        """
    return hashlib.sha256(f'{settings.secret_key}{password}'.encode('utf8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str):
    """Сравнивает хеши проверяемого и настоящего пароля.

        Parameters
        ----------
        plain_password: str
            Проверяемый пароль.
        hashed_password: str
            Настоящий пароль
        """
    if get_password_hash(plain_password) != hashed_password:
        return False
    return True


async def authenticate_user(email: str, password: str, session: AsyncSession):
    """Проверяет пароль и в случае совпадения паролей,
       возвращает текущего пользователя.

        Parameters
        ----------
        email: str
            email.
        password: str
            Пароль
        """
    user_item = await UserRepository.get_user_by_email(email, session)
    if not user_item:
        return False
    if not verify_password(password, user_item[0][4]):
        return False
    return user_item


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    """Генерирует токен.

        Parameters
        ----------
        data: dict
            Словарь с данными.
        expires_delta: datetime.timedelta
            Настоящий пароль
        """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str):
    """Проверяет токен на действительность.
       Если время действия токена закончилось,
       вызывает исключение JWTError.
        Parameters
        ----------
        token: str
            Токен.
        """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except JWTError:
        return False
    return True


class UserRepository:
    """Репозиторий для сущности пользователь."""

    @classmethod
    async def get_user_by_email(cls, email: str, session: AsyncSession):
        """Возвращает объект пользователь по email.

        Parameters
        ----------
        email: str
            email.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
        query = select(Users_model).where(Users_model.c.email == email)
        exists_user = await session.execute(query)
        exists_user = exists_user.all()
        if len(exists_user) > 0:
            return exists_user
        return False
    
    @classmethod
    async def get_user_by_id(cls, user_id: str, session: AsyncSession):
        """Возвращает объект пользователь по id.

        Parameters
        ----------
        user_id: str
            id пользователя.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
        query = select(Users_model).where(Users_model.c.id == user_id)
        exists_user = await session.execute(query)
        exists_user = exists_user.all()
        if len(exists_user) > 0:
            return exists_user
        return False

    @classmethod
    async def create_user(
        cls,
        name: str,
        surname: str,
        email: str,
        password: str,
        role: str,
        session: AsyncSession,
    ):
        """Создает нового пользователя.

        Parameters
        ----------
        name: str
            Имя пользователя.
        surname: str
            Фамилия пользователя.
        email: str
            email пользователя.
        password: str
            Пароль пользователя.
        role: int
            id роли пользователя.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
        exists_user = await cls.get_user_by_email(email, session)
        if exists_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь с email {email} уже существует',
            )
        role_object = await RoleRepository.get_role_by_name(role, session)
        if not role_object:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Роли {role} не существует',
            )
        try:
            query = Users_model.insert().values(
                name=name,
                surname=surname,
                email=email,
                password=get_password_hash(password),
                role=role_object[0][0],
            )
            await session.execute(query)
            await session.commit()
        except Exception as some_ex:
            print(some_ex)
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        try:
            user = await cls.get_user_by_email(email, session)
            return UserModelResp(
                name=user[0][1],
                surname=user[0][2],
                email=user[0][3],
            )
        except Exception as some_ex:
            print(some_ex)
            return {"detail": "Ошибка при отправке ответа"}
        
    @classmethod
    async def update_user(
        cls,
        name: str,
        surname: str,
        email: str,
        role: str,
        user_id: str,
        session: AsyncSession,
    ):
        """Обновляет данные пользователя.

        Parameters
        ----------
        name: str
            Имя пользователя.
        surname: str
            Фамилия пользователя.
        email: str
            email пользователя..
        role: int
            id роли пользователя.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
        exists_new_email = await cls.get_user_by_email(email, session)
        if exists_new_email:
            if exists_new_email[0][0] != int(user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Пользователь с email {email} уже существует',
                )
        exists_user = await cls.get_user_by_id(int(user_id), session)

        if exists_user:
            role_object = await RoleRepository.get_role_by_name(role, session)
            if not role_object:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Роли {role} не существует',
                )
            try:
                query = Users_model.update().where(
                    Users_model.c.id == int(user_id),
                ).values(
                    name=name,
                    surname=surname,
                    email=email,
                    role=role_object[0][0],
                )
                await session.execute(query)
                await session.commit()

            except Exception:
                await session.rollback()
                return {"detail": 'Произошла ошибка при работе с базой данных'}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь не найден",
            )
        try:
            user = await cls.get_user_by_id(int(user_id), session)
            return UserUpdateResp(
                new_name=user[0][1],
                new_surname=user[0][2],
                new_email=user[0][3],
                new_role=user[0][5],
            )
        except Exception:
            return {"detail": "Ошибка при отправке ответа"}
        
    @classmethod
    async def get_users_list(cls, session: AsyncSession):
        """Возвращает список пользователей.

        Parameters
        ----------
        session: str
            Сессия соединения с базой данных.
        """
        query = select(Users_model)
        users_list = await session.execute(query)
        users_list = users_list.all()
        if len(users_list) == 0:
            return {}
        response = {}

        for i in range(len(users_list)):
            response[users_list[i][0]] = {
                "id": users_list[i][0],
                "name": users_list[i][1],
                "surname": users_list[i][2],
                "email": users_list[i][3],
                "role": users_list[i][5],
            }
        return response
    
    @classmethod
    async def delete_user(cls, target_user_id: str, session: AsyncSession):
        """Удаляет пользователя по id.

        Parameters
        ----------
        target_user_id: str
            id пользователя.
        session: AsyncSession
            Сессия соединения с базой данных.
        """
        exists_user = await cls.get_user_by_id(int(target_user_id), session)
        if not exists_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь не найден',
            )
        try:
            query = Users_model.delete().where(Users_model.c.id == int(target_user_id))
            await session.execute(query)
            await session.commit()
            return {
                "status": True,
                "message": "Пользователь успешно удален"
            }
        except Exception:
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        
    @classmethod
    async def registration_user(
        cls,
        name: str,
        surname: str,
        email: str,
        password: str,
        session: AsyncSession,
    ):
        """Создает нового пользователя.

        Parameters
        ----------
        name: str
            Имя пользователя.
        surname: str
            Фамилия пользователя.
        email: str
            email пользователя.
        password: str
            Пароль пользователя.
        session: AsyncSession
            Сессия соединения с базой данных.
        """

        exists_user = await cls.get_user_by_email(email, session)
        if exists_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пользователь с email {email} уже существует',
            )
        role_object = await RoleRepository.get_role_by_name('user', session)
        if not role_object:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Роли не существует',
            )
        try:
            query = Users_model.insert().values(
                name=name,
                surname=surname,
                email=email,
                password=get_password_hash(password),
                role=role_object[0][0],
            )
            await session.execute(query)
            await session.commit()
        except Exception as some_ex:
            print(some_ex)
            await session.rollback()
            return {"detail": 'Произошла ошибка при работе с базой данных'}
        try:
            user = await cls.get_user_by_email(email, session)
            return UserModelResp(
                name=user[0][1],
                surname=user[0][2],
                email=user[0][3],
            )
        except Exception as some_ex:
            print(some_ex)
            return {"detail": "Ошибка при отправке ответа"}