from pprint import pprint
from fastapi import FastAPI, Path, Query, Body
import uvicorn


app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Moscow", "name": "moscow"}
]


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(default=None, description="Идентификатор отеля"),
):
    if id:
        return [hotel for hotel in hotels if hotel["id"] == id]
    else:
        return hotels


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return {"status": "OK"}
    return {"status": "ERROR"}


@app.post("/hotels")
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


@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int = Path(embed=True, description="Идентификатор отеля"),
        title: str = Body(embed=True),
        name: str = Body(embed=True)
    ):
    """Меняет все параметры одного отеля"""
    for hotel in hotels:
        print(hotel)
        print(f"{hotel_id=}, {title=}, {name=}")
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            pprint(hotels)
            return {"status": "OK"}
    return {"status": "ERROR. Hotel not found"}





if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
