from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Envs(BaseSettings):
    DATABASE_URL: str
    ENCRYPTION_KEY: str
    SECRET_KEY: str
    JWT_EXPIRATION: str = Field(pattern=r"^\d+(d|h|min|s)$")
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


try:
    settings = Envs()  # type: ignore
except ValidationError as e:
    print("Error to load environment envs: ", e)
    raise
