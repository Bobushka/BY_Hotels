from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


# Создадим движок для подключения к нашей БД
engine = create_async_engine(settings.DB_URL)

# Создадим фабрику, которая генерирует сессии. По сути, Сессия == Транзакция
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

# Создаем пустой класс для моделей. 
# В нем наследован парамер metadata, который булет содержать все данные о наших моделях.
class BaseModel(DeclarativeBase):
    pass


def main():
    # Пример сырого SQL-запроса через Алхимию:
    from sqlalchemy import text
    import asyncio

    async def func():
        async with engine.begin() as conn:
            res = await conn.execute(text("SELECT version()"))  # запрос возвращает версию PostgreSQL
            # res - это генератор, нам из него нужна только одна строка:
            print(res.fetchone())

    asyncio.run(func())
    # вызывается строкой в main.py: from app.database import *


if __name__ == "__main__":
    main()