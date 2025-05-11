# ./hotels.py

from fastapi import Query, Body, APIRouter
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
    id: int | None = Query(default=None, description="Идентификатор отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
    page: int = 0,
    per_page: int = 3
):
    """Возвращает список отелей. Если не передан ни один параметр, то возвращает первую страницу пагинации и на ней первые 10 отелей. Если page и/или per_page переданы, то возвращает соответствующую страницу пагинации с соответствующим количеством отелей на ней."""
    hotels_ = [] 
    # Реализуем случай запроса конкретного отеля (id и/или title переданы)
    if id or title:
        for hotel in hotels:
            if id and hotel["id"] != id:
                continue
            if title and hotel["title"] != title:
                continue
            hotels_.append(hotel)
            return hotels_
    # Реализуем случай передачи страницы пагинации
    else:
        for hotel in hotels[page * per_page: page * per_page + per_page]:
            hotels_.append(hotel)
        return hotels_


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return {"status": "OK"}
    return {"status": "ERROR"}


@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples=hotelsPOSTexample)):
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    """Меняет все параметры одного отеля"""
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
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
    """Меняет один из параметров или оба параметра одного отеля"""
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel:
        if hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel_data.name:
            hotel["name"] = hotel_data.name
        return {"status": "OK"}
    return {"status": "ERROR. Hotel not found"}
