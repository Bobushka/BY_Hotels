from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# определяем абсолютный путь до корня проекта
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property  # декоратор указывает на то, что это не метод, а атрибут
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property  # это синхронный драйвер БД, он необходим для работы алембика
    def DB_URL_SYNC(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        # pathlib позволяет формировать путь с помощью оператора "/", аналогично os.path.join()
        # Такой способ задания пути к .env файлу делает загрузку конфигураций стабильной и понятной. Путь до корня проекта вычисляется относительно расположения самого модуля config.py в проекте, а не от текущей рабочей директории процесса.
        # Файл с переменными окружения будет одинаково определяться в корне проекта при любом способе запуска приложения (через uvicorn, в Docker контейнере или каком-то специальном тестовом окружении). 
        # Использование pathlib гарантирует, что определение пути работает одинаково для всех типов операционных систем: Linux, macOS, Windows.
        env_file=BASE_DIR / ".env",
    )


settings = Settings()  # type: ignore[call-arg]
"""
Выше не обычный комментарий, а специальная подсказка для type checker.
# type: ignore[call-arg] говорит Pylance: “игнорируй предупреждение про аргументы у этой строки”, потому что значения приходят из .env во время выполнения, а статический анализ этого не знает.
"""
