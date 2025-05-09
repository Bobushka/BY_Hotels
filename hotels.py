from fastapi import Query, Body, Path, APIRouter
from shemas.hotels import Hotel, HotelPATCH


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
):
    if id:
        return [hotel for hotel in hotels if hotel["id"] == id]
    else:
        return hotels


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return {"status": "OK"}
    return {"status": "ERROR"}


@router.post("")
def create_hotel(hotel_data: Hotel):
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
