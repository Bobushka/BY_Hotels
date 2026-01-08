# ./examples.py

from fastapi.openapi.models import Example

# Формируем примеры в формате FastAPI Example, чтобы тип совпадал с openapi_examples.
hotelsPOSTexample = {
    "1": Example(
        summary="Сочи",
        value={
            "title": "Отель Сочи 5 звезд у моря",
            "location": "ул. Моря, 1",
        },
    ),
    "2": Example(
        summary="Дубай",
        value={
            "title": "Отель Дубай У фонтана",
            "location": "ул. Шейха, 2",
        },
    ),
}
