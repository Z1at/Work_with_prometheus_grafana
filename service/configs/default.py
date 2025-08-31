from os import getenv
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    """
        Default configs for application.
    """

    load_dotenv()
    PATH_PREFIX: str = getenv("APP_PATH_PREFIX", "/api")
    APP_HOST: str = getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = getenv("APP_PORT", 8080)

    POSTGRES_DB: str = getenv("POSTGRES_DB", "fastapi_db")
    POSTGRES_HOST: str = getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = getenv("POSTGRES_USER", "user")
    POSTGRES_PORT: int = int(getenv("POSTGRES_PORT", "5432")[-4:])
    POSTGRES_PASSWORD: str = getenv("POSTGRES_PASSWORD", "hackme")

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )
