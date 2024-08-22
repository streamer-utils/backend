import contextlib
from typing import Any, AsyncIterator, Generic, TypeVar

from sqlalchemy import Delete, Select, Update
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.domain.base import BaseStructure
from app.models.base import Base
from core.db import sessionmanager

from .base import BaseRepository


T = TypeVar("T", bound=Base)
R = TypeVar("R", bound=BaseStructure)
SELECT_T = TypeVar("SELECT_T", bound=Select)
UPDATE_T = TypeVar("UPDATE_T", bound=Update)
DELETE_T = TypeVar("DELETE_T", bound=Delete)


class SqlAlchemyRepository(Generic[T], BaseRepository):
    MODEL: type[T]
    DOES_NOT_EXIST: type[SQLAlchemyError] = NoResultFound

    def __init__(self):
        ...

    @classmethod
    @contextlib.asynccontextmanager
    async def transaction(cls) -> AsyncIterator[dict]:
        async with sessionmanager.session() as session:
            async with session.begin():
                yield {"custom_session": session}

    @classmethod
    @contextlib.asynccontextmanager
    async def session(cls, custom_session: AsyncSession | None = None) -> AsyncIterator[AsyncSession]:
        if custom_session:
            yield custom_session
            return

        async with sessionmanager.session() as session:
            yield session

    @classmethod
    @contextlib.asynccontextmanager
    async def begin(cls, session: AsyncSession, make_nested: bool = False) -> AsyncIterator[AsyncSessionTransaction]:
        in_transaction = session.in_transaction()

        if in_transaction and not make_nested:
            tr = session.get_transaction()
            assert tr

            yield tr
            return

        if in_transaction:
            method = session.begin_nested
        else:
            method = session.begin

        async with method() as transaction:
            yield transaction

    @classmethod
    def _add_filters(
        cls, stmt: SELECT_T | UPDATE_T | DELETE_T, filters: dict[str, Any]
    ) -> SELECT_T | UPDATE_T | DELETE_T:
        for key, value in filters.items():
            field_name, _, sign = key.partition("__")

            if sign == "in":
                stmt = stmt.where(getattr(cls.MODEL, field_name).in_(value))
            elif sign == "not":
                stmt = stmt.where(getattr(cls.MODEL, field_name) != value)
            else:
                stmt = stmt.where(getattr(cls.MODEL, field_name) == value)

        return stmt
