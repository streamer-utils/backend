from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column, Mapped

from app.models import Base
from app.domain.users import TwitchId


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    twitch_id: Mapped[TwitchId] = mapped_column(BigInteger, unique=True, index=True)
    twitch_login: Mapped[str] = mapped_column(String(length=32), unique=False)
