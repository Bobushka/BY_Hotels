# app/api/rooms.py

from fastapi import APIRouter, Body

from app.api.dependencies import DBDep
from app.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels")


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep):
    """
    Возвращает список номеров отеля.

    Args:
        hotel_id: Идентификатор отеля.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Список номеров указанного отеля.
    """
    # Получаем все номера, относящиеся к указанному отелю.
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    """
    Возвращает номер по его идентификатору в рамках отеля.

    Args:
        hotel_id: Идентификатор отеля.
        room_id: Идентификатор номера.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Данные номера, если он найден.
    """
    # Ищем номер по id и отелю, чтобы не получить номер из другого отеля.
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    """
    Создает номер в указанном отеле.

    Args:
        hotel_id: Идентификатор отеля.
        db: Менеджер БД для доступа к репозиториям.
        room_data: Данные номера из запроса.

    Returns:
        Статус операции и созданный номер.
    """
    # Собираем данные номера с привязкой к отелю.
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    # Сохраняем номер и фиксируем транзакцию.
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep,):
    """
    Полностью обновляет данные номера.

    Args:
        hotel_id: Идентификатор отеля.
        room_id: Идентификатор номера.
        room_data: Новые данные номера.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Статус операции.
    """
    # Формируем объект для полного обновления номера.
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    # Обновляем номер и фиксируем транзакцию.
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep,
):
    """
    Частично обновляет данные номера.

    Args:
        hotel_id: Идентификатор отеля.
        room_id: Идентификатор номера.
        room_data: Частичные данные номера.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Статус операции.
    """
    # Собираем только переданные поля для частичного обновления.
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    # Обновляем номер с учетом отеля и фиксируем транзакцию.
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    """
    Удаляет номер из указанного отеля.

    Args:
        hotel_id: Идентификатор отеля.
        room_id: Идентификатор номера.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Статус операции.
    """
    # Удаляем номер и фиксируем изменения.
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
