# app/api/auth.py

from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.api.dependencies import UserIdDep
from repositories.users import UsersRepository
from app.database import async_session_maker
from app.schemas.users import UserRequestAdd, UserAdd
from app.services.auth import AuthService

router = APIRouter(prefix="/auth")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    """
    Регистрирует пользователя по email и паролю.

    Args:
        data: данные регистрации (email и пароль).

    Returns:
        Словарь со статусом результата операции.
    """
    # Хэшируем пароль перед сохранением, чтобы не хранить его в открытом виде.
    hashed_password = AuthService().hash_password(data.password)
    # Формируем данные пользователя, которые будут сохранены в базе.
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            # Пишем пользователя в базу в рамках транзакции.
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except IntegrityError:
            # Откатываем транзакцию, чтобы корректно обработать дублирование email.
            await session.rollback()
            raise HTTPException(status_code=409, detail="Email already exists")
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    """
    Выполняет вход пользователя и выдает JWT access-токен.

    Args:
        data: данные для входа (email и пароль).
        response: объект ответа для установки cookie.

    Returns:
        Словарь с access-токеном.
    """
    async with async_session_maker() as session:
        # Ищем пользователя по email и получаем хэш пароля для проверки.
        try:
            user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        except NoResultFound:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        # Сверяем введенный пароль с сохраненным хэшем.
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        # Формируем токен доступа и возвращаем его пользователю.
        access_token = AuthService().create_access_token({"user_id": user.id})
        # Сохраняем токен в cookie для последующих запросов.
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIdDep):
    """
    Возвращает пользователя по идентификатору из зависимости авторизации.

    Args:
        user_id: идентификатор пользователя, полученный из зависимости.

    Returns:
        Pydantic-модель пользователя, если он найден,
        иначе None (если пользователя нет).
    """
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"Logout OK"}