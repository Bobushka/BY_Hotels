from app.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


# Создаем модель таблицы "Номера", которая отображает будущую реальную таблицу в БД
class RoomsOrm(BaseModel):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)  # уникальный первичный ключ
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))  # внешний ключ
    title: Mapped[str]
    description: Mapped[str | None]  # необязательный параметр
    price: Mapped[int]               # для упрощения цена без копеек
    quantity: Mapped[int]