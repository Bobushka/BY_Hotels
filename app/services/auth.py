# app/services/auth.py

from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from app.config import settings


class AuthService:
    """Вспомогательные методы авторизации: хэширование/проверка паролей и JWT-токены."""
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        """
        Создает JWT access-токен на основе входных данных.

        - Копирует входной словарь, чтобы не менять данные вызывающего кода.
        - Добавляет claim "exp" (время истечения) в UTC на основе настроек приложения,
          чтобы все сервисы интерпретировали срок жизни одинаково.
        - "exp" — стандартный JWT-claim, по которому библиотеки проверяют истечение токена.
        - Подписывает токен секретным ключом и алгоритмом из настроек, чтобы защитить от подмены.

        :param data: словарь с полезной нагрузкой (например, {"sub": user_id}).
        :return: строка JWT-токена.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode["exp"] = expire
        return jwt.encode(
            to_encode, 
            settings.JWT_SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )

    def hash_password(self, password: str) -> str:
        """
        Хэширует пароль безопасным алгоритмом (Argon2) через passlib.

        - Использует случайную соль и параметры алгоритма автоматически.
        - Соль и настройки сохраняются внутри строки хэша (это не секрет, а формат).
        - Храним только стойкий односторонний хэш, а не пароль в открытом виде.

        :param password: пароль в открытом виде.
        :return: строка хэша для хранения в базе.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """
        Проверяет пароль, сравнивая его с сохраненным хэшем.

        - Извлекает соль и параметры из строки хэша.
        - Пересчитывает хэш для введенного пароля и сравнивает результаты.
        - "соль" — случайная строка, добавляемая к паролю перед хэшированием,
          чтобы одинаковые пароли давали разные хэши и их нельзя было сравнивать по базе.
        - "медленная функция" — алгоритм, который намеренно считается долго (например, Argon2),
          чтобы усложнить перебор паролей и атаки по словарям/радужным таблицам.
        - Возвращает True/False в зависимости от совпадения.

        :param plain_password: пароль в открытом виде (ввод пользователя).
        :param hashed_password: сохраненный в базе хэш пароля.
        :return: True, если пароль корректный, иначе False.
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")
