from typing import TypedDict, cast

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, validate_token
from twitchAPI.type import AuthScope

from core.config import env_config
from app.serializers.auth import AuthorizeError, AuthorizeResponse
from app.repositories.users import UserRepository
from app.domain.users import UserCreate, TwitchId

import jwt


USER_SCOPE = [AuthScope.CHAT_READ]


def get_auth_url(base_url: str):
    twitch = Twitch(
        env_config.TWITCH_CLIENT_ID,
        env_config.TWITCH_SECRET_KEY
    )

    auth = UserAuthenticator(
        twitch,
        USER_SCOPE,
        force_verify=False,
        url=base_url
    )

    return auth.return_auth_url()


class ValidateResponse(TypedDict):
    client_id: str
    login: str
    scopes: list[str]
    user_id: str


async def authorize(base_url: str, code: str, scope: list[str]) -> AuthorizeResponse | AuthorizeError:
    twitch = await Twitch(env_config.TWITCH_CLIENT_ID, env_config.TWITCH_SECRET_KEY)
    target_scope = [AuthScope.CHANNEL_BOT]

    auth = UserAuthenticator(
        twitch,
        target_scope,
        force_verify=False,
        url=base_url
    )

    auth_result: tuple[str, str] | None = None

    try:
        auth_result = await auth.authenticate(user_token=code)
    except Exception as e:
        return AuthorizeError(error=str(e))

    if auth_result is None:
        return AuthorizeError(error="Invalid code")

    token, refresh_token = auth_result

    result = cast(ValidateResponse, await validate_token(token))

    user = await UserRepository.get_or_create(
        UserCreate(
            twitch_id=TwitchId(int(result["user_id"])),
            twitch_login=result["login"]
        )
    )

    token = jwt.encode(
        {
            "user_id": user.id,
            "twitch_id": user.twitch_id,
            "twitch_login": user.twitch_login
        },
        env_config.SECRET_KEY,
        algorithm="HS256"
    )

    return AuthorizeResponse(token=token)
