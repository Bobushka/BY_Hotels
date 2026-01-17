# ./main.py

from fastapi import FastAPI, Path, Query, Body
import uvicorn

import sys
from pathlib import Path

# Эта команда позволяет интерпретатору определить местонахождение файла main.py относительно его родителя и родителя его родителя. Без этого невозможны абсолютные импорты, невозможно создание экземпляра FastAPI и команда python app/main.py не выполнится:
sys.path.append(str(Path(__file__).parent.parent))

from app.api.hotels import router as router_hotels
from app.api.rooms import router as router_rooms
from app.api.auth import router as router_auth
from app.api.bookings import router as router_bookings


app = FastAPI(
    title="BY_Hotels",
    summary="https://lk.pytex.school/teach/control/stream/view/id/934873195",
    description="Второй курс Артема Шумейко",
)

app.include_router(router_auth, tags=["Auth"])
app.include_router(router_hotels, tags=["Hotels"])
app.include_router(router_rooms, tags=["Rooms"])
app.include_router(router_bookings, tags=["Bookings"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

