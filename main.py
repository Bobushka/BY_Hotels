from pprint import pprint
from fastapi import FastAPI, Path, Query, Body
import uvicorn


app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Moscow", "name": "moscow"}
]

# --------------------------------------------------------

import time, asyncio

@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync.start {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync.finish {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Start {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async.finish {id}: {time.time():.2f}")

# --------------------------------------------------------

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


@app.patch(
        path="/hotels/{hotel_id}",
        summary="Меняет один из параметров или оба параметра одного отеля",
        description="Частично обновляет данные одного отеля"  # можно использовать HTML
    )
def update_hotel(
        hotel_id: int = Path(embed=True, description="Идентификатор отеля"),
        title: str | None = Body(default=None, embed=True),
        name: str | None = Body(default=None, embed=True)
    ):
    """Меняет один из параметров или оба параметра одного отеля"""
    if title and name:
        for hotel in hotels:
            if hotel["id"] == hotel_id:
                hotel["title"] = title
                hotel["name"] = name
                return {"status": "OK"}
        return {"status": "ERROR. Hotel not found"}
    if title: 
        for hotel in hotels:
            if hotel["id"] == hotel_id:
                hotel["title"] = title
                return {"status": "OK"}
            return {"status": "ERROR(title). Hotel not found"}
    if name:
        for hotel in hotels:
            if hotel["id"] == hotel_id:
                hotel["name"] = name
                return {"status": "OK"}
            return {"status": "ERROR(name). Hotel not found"}
    return {"status": "ERROR. At least one parameter must be provided"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
