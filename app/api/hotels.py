# app/api/hotels.py

from fastapi import Query, Body, APIRouter

from app.api.dependencies import PaginationDep, DBDep
from app.schemas.hotels import HotelAdd, HotelPatch
from app.api.examples import hotelsPOSTexample


router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    sub_title: str | None = Query(default=None, description="Подстрока названия отеля в любом регистре"),
    sub_location: str | None = Query(default=None, description="Подстрока адреса отеля в любом регистре")
):
    """
    Возвращает список отелей.

    Args:
        pagination: Параметры пагинации.
        db: Менеджер БД для доступа к репозиториям.
        sub_title: Подстрока названия отеля в любом регистре.
        sub_location: Подстрока адреса отеля в любом регистре.

    Returns:
        Список отелей.
    """
    # Читаем список отелей с учетом фильтров и пагинации.
    return await db.hotels.get_all(
        location=sub_location,
        title=sub_title,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    """
    Возвращает один отель по его id.

    Args:
        hotel_id: идентификатор отеля в БД.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        JSON с параметрами одного отеля.
    """
    # Ищем отель по идентификатору.
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples=hotelsPOSTexample),
):
    """
    Создает новый отель.

    Args:
        db: Менеджер БД для доступа к репозиториям.
        hotel_data: Данные отеля из запроса.

    Returns:
        Статус операции.
    """
    # Создаем новый отель и сохраняем его в базе.
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
    hotel_id: int, 
    hotel_data: HotelAdd,
    db: DBDep
):
    """
    Меняет все параметры одного отеля.

    Args:
        hotel_id: Идентификатор отеля.
        hotel_data: Новые данные отеля.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Статус операции.
    """
    # Полностью обновляем данные отеля по идентификатору.
    hotel = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
        path="/{hotel_id}",
        summary="Меняет один из параметров или оба параметра одного отеля",
        description="Частично обновляет данные одного отеля"  # можно использовать HTML
    )
async def partially_edit_hotel(
    hotel_id: int, 
    hotel_data: HotelPatch,
    db: DBDep,
):
    """
    Меняет один из параметров или оба параметра одного отеля.

    Args:
        hotel_id: Идентификатор отеля.
        hotel_data: Частичные данные отеля.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Статус операции.
    """
    # Обновляем только переданные поля отеля.
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    """
    Удаляет отель по идентификатору.

    Args:
        hotel_id: Идентификатор отеля.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Статус операции.
    """
    # Удаляем отель и фиксируем изменения.
    hotel = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
