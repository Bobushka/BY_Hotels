# app/api/hotels.py

from fastapi import Query, Body, APIRouter
from typing import Annotated

from app.api.dependencies import PaginationDep
from app.shemas.hotels import HotelAdd, HotelPATCH
from app.api.examples import hotelsPOSTexample
from database import engine, async_session_maker
from app.repositories.hotels import HotelsRepository


router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    sub_title: str | None = Query(default=None, description="Подстрока названия отеля в любом регистре"),
    sub_location: str | None = Query(default=None, description="Подстрока адреса отеля в любом регистре")
):
    """
    Возвращает список отелей.

    Args:
        pagination: Параметры пагинации.
        sub_title: Подстрока названия отеля в любом регистре.
        sub_location: Подстрока адреса отеля в любом регистре.

    Returns:
        Список отелей.
    """
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=sub_location,
            title=sub_title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1)
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    """
    Возвращает один отель по его id.

    Args:
        hotel_id: идентификатор отеля в БД.

    Returns:
        JSON с параметрами одного отеля.
    """
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples=hotelsPOSTexample)):
    """
    Создает новый отель.

    Args:
        hotel_data: Данные отеля из запроса.

    Returns:
        Статус операции.
    """
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    """
    Меняет все параметры одного отеля.

    Args:
        hotel_id: Идентификатор отеля.
        hotel_data: Новые данные отеля.

    Returns:
        Статус операции.
    """
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
        path="/{hotel_id}",
        summary="Меняет один из параметров или оба параметра одного отеля",
        description="Частично обновляет данные одного отеля"  # можно использовать HTML
    )
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    """
    Меняет один из параметров или оба параметра одного отеля.

    Args:
        hotel_id: Идентификатор отеля.
        hotel_data: Частичные данные отеля.

    Returns:
        Статус операции.
    """
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    """
    Удаляет отель по идентификатору.

    Args:
        hotel_id: Идентификатор отеля.

    Returns:
        Статус операции.
    """
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
