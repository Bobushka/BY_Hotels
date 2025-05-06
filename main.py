from pprint import pprint
from fastapi import FastAPI, Path, Query, Body
import uvicorn
from hotels import router as router_hotels

app = FastAPI()

app.include_router(router_hotels, tags=["Hotels"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
