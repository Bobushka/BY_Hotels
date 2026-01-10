# ./hotels.py

from fastapi import Query, Body, APIRouter
from typing import Annotated
from sqlalchemy import insert, select, func

from app.api.dependencies import PaginationDep
from app.shemas.hotels import Hotel, HotelPATCH
from app.api.examples import hotelsPOSTexample
from database import engine, async_session_maker
from app.models.hotels import HotelsORM


router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название отеля"),
    sub_location: str | None = Query(default=None, description="Подстрока адреса отеля")
):
    """
    Возвращает список отелей.

    Args:
        pagination: Параметры пагинации.
        id: Идентификатор отеля.
        title: Название отеля.

    Returns:
        Список отелей.
    """
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if title:
            query = query.filter_by(title=title)
        if sub_location:
            query = (
                query
                .where(func.lower(HotelsORM.location)  # приводим к нижнему регистру содержание колонки
                .like(f"%{sub_location.lower()}%"))  # приводим к нижнему регистру запрос пользователя
            )
        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    """
    Удаляет отель по идентификатору.

    Args:
        hotel_id: Идентификатор отеля.

    Returns:
        Статус операции.
    """
    # Ищем отель по идентификатору, чтобы удалить первую найденную запись.
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return {"status": "OK"}
    # Если отель не найден, возвращаем статус ошибки без модификации списка.
    return {"status": "ERROR"}


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples=hotelsPOSTexample)):
    """
    Создает новый отель.

    Args:
        hotel_data: Данные отеля из запроса.

    Returns:
        Статус операции.
    """
    async with async_session_maker() as session:
        add_hotel_query = insert(HotelsORM).values(**hotel_data.model_dump())
        print(add_hotel_query.compile(bind=engine, compile_kwargs={"literal_binds": True}))  # эта строка позволяет увидеть в терминале реальный SQL-запрос который алхимия отправляет в БД. Это полезно для дебага.
        await session.execute(add_hotel_query)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    """
    Меняет все параметры одного отеля.

    Args:
        hotel_id: Идентификатор отеля.
        hotel_data: Новые данные отеля.

    Returns:
        Статус операции.
    """
    # Находим отель по идентификатору, чтобы заменить все его поля.
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    # Полностью обновляем значения полей, чтобы отразить входные данные.
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
        path="/{hotel_id}",
        summary="Меняет один из параметров или оба параметра одного отеля",
        description="Частично обновляет данные одного отеля"  # можно использовать HTML
    )
def update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
    ):
    """
    Меняет один из параметров или оба параметра одного отеля.

    Args:
        hotel_id: Идентификатор отеля.
        hotel_data: Частичные данные отеля.

    Returns:
        Статус операции.
    """
    # Ищем отель по идентификатору, чтобы применить частичное обновление.
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel:
        # Обновляем только переданные поля, чтобы сохранить остальные значения.
        if hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel_data.name:
            hotel["name"] = hotel_data.name
        return {"status": "OK"}
    # Если отель не найден, возвращаем ошибку без изменений.
    return {"status": "ERROR. Hotel not found"}
