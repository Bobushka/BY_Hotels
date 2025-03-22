from fastapi import FastAPI, Query
import uvicorn


app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Dubai"},
    {"id": 3, "title": "Moscow"}
]

@app.get("/hotels")
def get_hotels(
    title: str | None = Query(description="Search by title")
):
    return [hotel for hotel in hotels if hotel["title"] == title]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
