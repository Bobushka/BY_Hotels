from repositories.base import BaseRepository
from app.models.rooms import RoomsORM


class RoomsRepository(BaseRepository):
    model = RoomsORM