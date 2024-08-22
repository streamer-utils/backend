from typing import Awaitable, Callable, ParamSpec, TypeVar

from sqlalchemy.exc import NoResultFound


_FuncParams = ParamSpec("_FuncParams")
_ReturnType = TypeVar("_ReturnType")


def _or_none(
    func: Callable[_FuncParams, Awaitable[_ReturnType]]
) -> Callable[_FuncParams, Awaitable[_ReturnType | None]]:
    if isinstance(func, classmethod):

        async def handler(*args: _FuncParams.args, **kwargs: _FuncParams.kwargs) -> _ReturnType | None:
            try:
                return await func.__func__(*args, **kwargs)  # type: ignore
            except NoResultFound:
                return None

        return classmethod(handler)  # type: ignore

    async def handler(*args: _FuncParams.args, **kwargs: _FuncParams.kwargs) -> _ReturnType | None:
        try:
            return await func(*args, **kwargs)
        except NoResultFound:
            return None

    return handler
