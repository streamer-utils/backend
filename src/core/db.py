import contextlib
from typing import AsyncGenerator, AsyncIterator
from urllib.parse import quote

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from core.config import env_config


DATABASE_URL = (
    f"postgresql+asyncpg://{env_config.POSTGRES_USER}:{quote(env_config.POSTGRES_PASSWORD)}@"
    f"{env_config.POSTGRES_HOST}:{env_config.POSTGRES_PORT}/{env_config.POSTGRES_DB}"
)

ALEMBIC_DATABASE_URL = (
    f"postgresql://{env_config.POSTGRES_USER}:{quote(env_config.POSTGRES_PASSWORD)}@"
    f"{env_config.POSTGRES_HOST}:{env_config.POSTGRES_PORT}/{env_config.POSTGRES_DB}"
)


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine:
            await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise RuntimeError("Database is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise RuntimeError("Database is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session
