from sqlalchemy import select

from app.repositories.clients.alchemy import SqlAlchemyRepository
from app.repositories.clients.alchemy_utils import _or_none
from app.models.users import User as UserModel
from app.domain.users import User, UserCreate, TwitchId


class UserRepository(SqlAlchemyRepository[UserModel]):
    MODEL = UserModel

    @classmethod
    async def get(cls, id: int) -> User:
        async with cls.session() as session:
            stmt = select(cls.MODEL).where(cls.MODEL.id == id)

            result = await session.execute(stmt)

            data = result.unique().scalars().one()
            return User.model_validate(data, from_attributes=True)

    @classmethod
    async def get_by_twitch_id(cls, twitch_id: TwitchId) -> User:
        async with cls.session() as session:
            stmt = select(cls.MODEL).where(cls.MODEL.twitch_id == twitch_id)

            result = await session.execute(stmt)

            data = result.unique().scalars().one()
            return User.model_validate(data, from_attributes=True)

    get_by_twitch_id_or_none = _or_none(get_by_twitch_id)

    @classmethod
    async def create(cls, data: UserCreate) -> User:
        async with cls.session() as session:
            obj = cls.MODEL(**data.model_dump())

            session.add(obj)

            await session.commit()
            await session.refresh(obj)

            return User.model_validate(obj, from_attributes=True)

    @classmethod
    async def get_or_create(cls, data: UserCreate) -> User:
        user = await cls.get_by_twitch_id_or_none(data.twitch_id)
        if user is not None:
            return user

        return await cls.create(data)
