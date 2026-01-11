from pydantic import BaseModel as SH_BaseModel
from sqlalchemy import select, insert, update, delete
from typing import ClassVar, Type

from app.database import BaseModel as DB_BaseModel
from app.models.hotels import HotelsORM


class BaseRepository:
    # покажем линтеру что model это переменная, относящаяся к классу BaseModel. Иначе ругается.
    model: ClassVar[Type[DB_BaseModel]]

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def add(self, data: SH_BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()
    
    async def edit(self, data: SH_BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
