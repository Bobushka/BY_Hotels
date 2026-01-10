from repositories.base import BaseRepository
from app.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
    model = HotelsORM