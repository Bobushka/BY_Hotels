from fastapi import FastAPI, Path, Query, Body
import uvicorn
import time, asyncio
import threading

app = FastAPI()


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Threads: {threading.active_count()}")
    print(f"sync.start {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync.finish {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Threads: {threading.active_count()}")
    print(f"async. Start {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async.finish {id}: {time.time():.2f}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)