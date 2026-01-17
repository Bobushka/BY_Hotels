# app/models/bookings.py

from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from app.database import BaseModel


class BookingsOrm(BaseModel):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)  # уникальный первичный ключ
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # внешний ключ
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))  # внешний ключ
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]               # цена за одну ночь

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days