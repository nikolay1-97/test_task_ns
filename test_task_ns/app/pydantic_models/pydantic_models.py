"""Модуль со схемами данных запрсов и ответов."""
from pydantic import BaseModel
import uuid

class UserModel(BaseModel):
    """Модель данных создания пользователя."""

    name: str
    surname: str
    email: str
    password: str
    role: str


class UserModelResp(BaseModel):
    """Модель ответа создания нового экземпляра сущности пользователь."""
    name: str
    surname: str
    email: str

class UserUpdate(BaseModel):
    """Модель для обновления данных пользователя."""
    name: str
    surname: str
    email: str
    role: str

class UserUpdateResp(BaseModel):
    """Модель ответа обновления пользователя."""
    new_name: str
    new_surname: str
    new_email: str
    new_role: int


class LoginModel(BaseModel):
    """Модель для данных входа в систему."""
    email: str
    password: str


class RegistrationModel(BaseModel):
    """Модель данных регистрации пользователей."""
    name: str
    surname: str
    email: str
    password: str