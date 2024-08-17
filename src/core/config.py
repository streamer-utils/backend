from typing import Optional

from pydantic_settings import BaseSettings


class EnvConfig(BaseSettings):
    ALLOW_HOST: str = ""

    SENTRY_DSN: Optional[str] = None


env_config = EnvConfig()  # type: ignore
