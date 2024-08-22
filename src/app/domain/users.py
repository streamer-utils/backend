from typing import NewType

from pydantic import BaseModel


TwitchId = NewType("TwitchId", int)


class User(BaseModel):
    id: int

    twitch_id: TwitchId
    twitch_login: str


class UserCreate(BaseModel):
    twitch_id: TwitchId
    twitch_login: str
