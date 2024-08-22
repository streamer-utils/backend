from sqlalchemy import select

from app.repositories.clients.alchemy import SqlAlchemyRepository
from app.models.users import User as UserModel
from app.domain.users import User, UserCreate, TwitchId


class UserRepository(SqlAlchemyRepository[UserModel]):
    model = UserModel

    @classmethod
    async def get(cls, id: int) -> User:
        async with cls.session() as session:
            stmt = select(cls.model).where(cls.model.id == id)

            result = await session.execute(stmt)

            data = result.unique().scalars().one()
            return User.model_validate(data, from_attributes=True)

    @classmethod
    async def get_by_twitch_id(cls, twitch_id: TwitchId) -> User:
        async with cls.session() as session:
            stmt = select(cls.model).where(cls.model.twitch_id == twitch_id)

            result = await session.execute(stmt)

            data = result.unique().scalars().one()
            return User.model_validate(data, from_attributes=True)

    @classmethod
    async def create(cls, data: UserCreate) -> User:
        async with cls.session() as session:
            obj = cls.MODEL(**data.model_dump())

            session.add(data)

            await session.commit()

            return User.model_validate(obj, from_attributes=True)

    @classmethod
    async def get_or_create(cls, data: UserCreate) -> User:
        user = await cls.get_by_twitch_id(data.twitch_id)
        if user is not None:
            return user

        return await cls.create(data)
