from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    """Параметры пагинации."""
    page: Annotated[int | None, Query(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[int | None, Query(default=3, ge=1, le=10, description="Количество элементов на странице")]

    # TBD: разберись почему в /docs не отображаются description параметров, заданных через Annotated

PaginationDep = Annotated[PaginationParams, Depends()]  # Pagination Dependency Parameter
