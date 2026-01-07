from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings


engine = create_async_engine(settings.DB_URL)


# =============================================================================
# Далее пример сырого SQL-запроса через Алхимию:
from sqlalchemy import text
import asyncio

async def func():
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT version()"))  # запрос возвращает версию PostgreSQL
        # res - это генератор, нам из него нужна только дна строка:
        print(res.fetchone())

asyncio.run(func())
# вызывается строкой в main.py: from app.database import *
# =============================================================================