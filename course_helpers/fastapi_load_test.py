# перед использованием переименовать в main.py и переместить в корневой каталог
# запуск из терминала: 1) запустить окружение 2) python main.py

from fastapi import FastAPI
import uvicorn
import time, asyncio
import threading

app = FastAPI()


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync.Threads_: {threading.active_count()}")
    print(f"sync.Start_ {id}: {time.time():.2f}")  # формат два знака после запятой
    time.sleep(3)
    print(f"sync.Finish {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async.Threads_: {threading.active_count()}")
    print(f"async.Start_ {id}: {time.time():.2f}")
    await asyncio.sleep(3)  # то же самое что и time.sleep(3), только в асинхронной реализации
    print(f"async.Finish {id}: {time.time():.2f}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)