from repositories.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema: type[Room] = Room

    # определим отдельный метод для номеров, иначе линтер ругается в api/booking.py
    async def get_room(self, **filter_by) -> Room:
        """
        Возвращает номер по фильтрам или выбрасывает ошибку, если он не найден.

        Args:
            **filter_by: параметры фильтрации для поиска номера.

        Returns:
            Номер в виде Pydantic-схемы.

        Raises:
            NoResultFound: если номер не найден.
        """
        # Формируем запрос на поиск номера по переданным фильтрам.
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one()
        # Преобразуем ORM-объект в Pydantic-схему.
        return self.schema.model_validate(model)
