# ./examples.py

from fastapi.openapi.models import Example

# Формируем примеры в формате FastAPI Example, чтобы тип совпадал с openapi_examples.
hotelsPOSTexample = {
    "1": Example(
        summary="Сочи",
        value={
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya",
        },
    ),
    "2": Example(
        summary="Дубай",
        value={
            "title": "Отель Дубай У фонтана",
            "name": "dubai_fountain",
        },
    ),
}
