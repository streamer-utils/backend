from typing import Optional

from pydantic_settings import BaseSettings


class EnvConfig(BaseSettings):
    ALLOW_HOST: str = ""

    SECRET_KEY: str = "debug"

    SENTRY_DSN: Optional[str] = None

    POSTGRES_USER: str = "debug"
    POSTGRES_PASSWORD: str = "debug"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "streamers_utils"

    TWITCH_CLIENT_ID: str = ""
    TWITCH_SECRET_KEY: str = ""


env_config = EnvConfig()  # type: ignore
