"""Операции с данными для сущности роль."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_sources.models import Roles_model

class RoleRepository:
    """Репозиторий для сущности роль."""

    @classmethod
    async def get_role_by_name(cls, role_name: str, session: AsyncSession):
        """Возвращает объект роль по имени.

            Parameters
            ----------
            role_name: str
                Имя роли.
            session: AsyncSession
                Сессия соединения с базой данных.
        """
        query = select(Roles_model).where(Roles_model.c.name == role_name)
        exists_role = await session.execute(query)
        exists_role = exists_role.all()
        if len(exists_role) > 0:
            return exists_role
        return False
    
    @classmethod
    async def get_role_by_id(cls, role_id: str, session: AsyncSession):
        """Возвращает объект роль по id

            Parameters
            ----------
            role_id: str
                ID роли.
            session: AsyncSession
                Сессия соединения с базой данных.
        """
        query = select(Roles_model).where(Roles_model.c.id == role_id)
        exists_role = await session.execute(query)
        exists_role = exists_role.all()
        if len(exists_role) > 0:
            return exists_role
        return False
    