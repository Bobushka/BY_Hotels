# app/api/auth.py

from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.api.dependencies import UserIdDep, DBDep
from app.schemas.users import UserRequestAdd, UserAdd
from app.services.auth import AuthService

router = APIRouter(prefix="/auth")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
        db: DBDep,
):
    """
    Регистрирует пользователя по email и паролю.

    Args:
        data: данные регистрации (email и пароль).
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Словарь со статусом результата операции.
    """
    # Хэшируем пароль перед сохранением, чтобы не хранить его в открытом виде.
    hashed_password = AuthService().hash_password(data.password)
    # Формируем данные пользователя, которые будут сохранены в базе.
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
        db: DBDep,
):
    """
    Выполняет вход пользователя и выдает JWT access-токен.

    Args:
        data: данные для входа (email и пароль).
        response: объект ответа для установки cookie.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Словарь с access-токеном.
    """
    # Ищем пользователя по email и получаем хэш пароля для проверки.
    try:
        user = await db.users.get_user_with_hashed_password(email=data.email)
    except NoResultFound:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    
    # Сверяем введенный пароль с сохраненным хэшем.
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    
    # Формируем токен доступа , сохраняем токен в cookie для последующих запросов.
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep
):
    """
    Возвращает пользователя по идентификатору из зависимости авторизации.

    Args:
        user_id: идентификатор пользователя, полученный из зависимости.
        db: Менеджер БД для доступа к репозиториям.

    Returns:
        Pydantic-модель пользователя, если он найден,
        иначе None (если пользователя нет).
    """
    # Получаем пользователя из базы по идентификатору.
    return await db.users.get_one_or_none(id=user_id)


@router.post("/logout")
async def logout_user(response: Response):
    """
    Выполняет выход пользователя, удаляя access-токен из cookies.

    Args:
        response: объект ответа для удаления cookie.

    Returns:
        Словарь со статусом операции.
    """
    # Удаляем access-токен из cookies, чтобы клиент больше не отправлял его.
    response.delete_cookie("access_token")
    return {"Logout OK"}
