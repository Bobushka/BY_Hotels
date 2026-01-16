from typing import List
from sqlalchemy import select, func
from app.schemas.hotels import Hotel
from repositories.base import BaseRepository
from app.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    # специфический для отелей метод прописываем здесь, а не в base.py:
    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> List[Hotel]:
        
        query = select(HotelsORM)
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        # эта строка позволяет увидеть в терминале реальный SQL-запрос который алхимия отправляет в БД. Это полезно для дебага:
        print(query.compile(compile_kwargs={"literal_binds": True}))  # 4DEBUG
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel) for hotel in result.scalars().all()]