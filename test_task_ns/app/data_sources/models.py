"""Модели таблиц базы данных."""
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import DB_URL

metadata = MetaData()
engine = create_async_engine(DB_URL)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session():
    async with async_session_maker() as session:
        yield session

#Модель данных для сущности пользователь.
Users_model = Table(
    "users",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String, nullable=False),
    Column('surname', String, nullable=False),
    Column('email', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('role', Integer, ForeignKey("roles.id"), nullable=False)
)

#Модель данных сущности роль.
Roles_model = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String, nullable=False, unique=True),
)
