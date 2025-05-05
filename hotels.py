from fastapi import Query, Body, Path, APIRouter


router = APIRouter(prefix="/hotels")


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Moscow", "name": "moscow"}
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
def create_hotel(
        title: str = Body(embed=True, description="Название отеля"),
        name: str = Body(embed=True, description="Название отеля на английском"),
    ):
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(
        hotel_id: int = Path(embed=True, description="Идентификатор отеля"),
        title: str = Body(embed=True),
        name: str = Body(embed=True)
    ):
    """Меняет все параметры одного отеля"""
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
    return {"status": "ERROR. Hotel not found"}


@router.patch(
        path="/{hotel_id}",
        summary="Меняет один из параметров или оба параметра одного отеля",
        description="Частично обновляет данные одного отеля"  # можно использовать HTML
    )
def update_hotel(
        hotel_id: int = Path(embed=True, description="Идентификатор отеля"),
        title: str | None = Body(default=None, embed=True),
        name: str | None = Body(default=None, embed=True)
    ):
    """Меняет один из параметров или оба параметра одного отеля"""
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id]
    if hotel:
        if title:
            hotel["title"] = title
        if name:
            hotel["name"] = name
        return {"status": "OK"}
    return {"status": "ERROR. Hotel not found"}
