# ./main.py

from fastapi import FastAPI, Path, Query, Body
import uvicorn

import sys
from pathlib import Path

# Эта команда позволяет интерпритатору определить местонахождение файла main.py относительно его родителя и родителя его родителя. Без этого невозможны абсолютные импорты, невозможно создание экземпляра FastAPI и команда python app/main.py не выполнится:
sys.path.append(str(Path(__file__).parent.parent))

from app.api.hotels import router as router_hotels
from app.config import settings

app = FastAPI()

app.include_router(router_hotels, tags=["Hotels"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
