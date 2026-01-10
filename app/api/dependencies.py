from fastapi import Depends, Query
from pydantic import BaseModel, Field
from typing import Annotated


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