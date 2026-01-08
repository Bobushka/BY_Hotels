from app.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


# Создаем модель таблицы "Отели", которая отображает будущую реальную таблицу в БД
class HotelsORM(BaseModel):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)  # уникальный первичный ключ
    title: Mapped[str] = mapped_column(String(100))  # максимум 100 символов в названии
    location: Mapped[str]  # на локацию ограничений нет, поэтому не нужна mapped_column