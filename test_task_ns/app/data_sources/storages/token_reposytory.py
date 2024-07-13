"""Репозиторий для сущности токен"""
from config import redis_instance

class TokenRepository():
    """Репозиторий для сущности токен."""

    REDIS_INSTANCE = redis_instance

    @classmethod
    async def write_token(cls, email: str, token: str):
        """Записывает токен в Redis.

            Parameters
            ----------
            email: str
                email.
            token: str
                Токен.
            """
        exists_token = cls.REDIS_INSTANCE.get(email)
        if exists_token:
            new_value = token
            await cls.REDIS_INSTANCE.set(email, new_value)
        else:
            await cls.REDIS_INSTANCE.set(email, token)

    @classmethod
    async def get_token(cls, email: str):
        """Возвращает токен по email.

        Parameters
        ----------
        email: str
            email.
        """
        token = await cls.REDIS_INSTANCE.get(email)
        return token

    @classmethod
    async def delete_token(cls, email: str):
        """Удаляет токен по email.

        Parameters
        ----------
        email: str
            email.
        """
        await cls.REDIS_INSTANCE.delete(email)
