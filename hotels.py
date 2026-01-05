# ./hotels.py

from fastapi import Depends, Query, Body, APIRouter
from typing import Annotated
from dependencies import PaginationDep
from shemas.hotels import Hotel, HotelPATCH
from examples import hotelsPOSTexample


router = APIRouter(prefix="/hotels")


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, description="Идентификатор отеля"),
    title: str | None = Query(default=None, description="Название отеля")
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
    # Готовим безопасные значения пагинации с учетом возможного None, чтобы умножение всегда было корректным.
    page = pagination.page if pagination.page is not None else 1
    per_page = pagination.per_page if pagination.per_page is not None else 3
    # Инициализируем контейнер для результата, чтобы собирать найденные элементы в одном списке.
    hotels_ = [] 
    # Обрабатываем запрос конкретного отеля по id и/или title, чтобы вернуть только совпадения.
    if id or title:
        # Последовательно фильтруем список отелей по всем переданным критериям.
        for hotel in hotels:
            if id and hotel["id"] != id:
                continue
            if title and hotel["title"] != title:
                continue
            hotels_.append(hotel)
            return hotels_
    # Обрабатываем запрос страницы пагинации, чтобы вернуть нужный срез списка отелей.
    else:
        # Берем срез по рассчитанным параметрам пагинации, чтобы сформировать страницу результата.
        for hotel in hotels[page * per_page: page * per_page + per_page]:
            hotels_.append(hotel)
        return hotels_


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
def create_hotel(hotel_data: Hotel = Body(openapi_examples=hotelsPOSTexample)):
    """
    Создает новый отель.

    Args:
        hotel_data: Данные отеля из запроса.

    Returns:
        Статус операции.
    """
    # Добавляем новый объект в конец списка, увеличивая идентификатор на основе последнего элемента.
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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
