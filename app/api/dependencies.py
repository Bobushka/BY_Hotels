# app/api/dependencies.py

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field
from typing import Annotated

from app.database import async_session_maker
from app.services.auth import AuthService
from app.utils.db_manager import DBManager


# ================= Получаем параметры пагинации ==============================

class PaginationParams(BaseModel):
    """Параметры пагинации."""
    page: Annotated[int, Field(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[int, Field(default=5, ge=1, le=10, description="Количество элементов на странице")]


def pagination_params(
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    per_page: int = Query(default=3, ge=1, le=10, description="Количество элементов на странице"),
) -> PaginationParams:
    """
    Создает параметры пагинации из query-параметров.

    Args:
        page: Номер страницы.
        per_page: Количество элементов на странице.

    Returns:
        Параметры пагинации.
    """
    # Собираем параметры пагинации в модель, чтобы использовать единый тип в обработчиках.
    return PaginationParams(page=page, per_page=per_page)


# Pagination Dependency Parameter
PaginationDep = Annotated[PaginationParams, Depends(pagination_params)]  


# ================= Получаем User ID из JWT-токена ============================

def get_token(request: Request) -> str:
    """
    Достает access-токен из cookies запроса.

    Args:
        request: входящий HTTP-запрос с cookies.

    Returns:
        Строка access-токена.

    Raises:
        HTTPException: если токен отсутствует.
    """
    # Берем access-токен из cookies; если его нет — запрещаем доступ.
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Нет токена доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    """
    Возвращает идентификатор пользователя из access-токена.

    Args:
        token: access-токен из cookies (через зависимость get_token).

    Returns:
        Идентификатор пользователя (user_id) из payload токена.
    """
    # Декодируем токен и извлекаем user_id из payload.
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]  


# ================= Получаем сессию БД ========================================

async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]