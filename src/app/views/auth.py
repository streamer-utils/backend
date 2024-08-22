from fastapi import APIRouter

from app.services.auth import get_auth_url, authorize
from app.serializers.auth import AuthorizeError, GetAuthorizeLinkResponse, AuthorizeResponse, AuthorizeData


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.get("/get_auth_url/")
async def get_auth_ur_handler(
    base_url: str
) -> GetAuthorizeLinkResponse:
    return GetAuthorizeLinkResponse(url=get_auth_url(base_url))


@auth_router.post("/authorize/")
async def authorize_handler(
    data: AuthorizeData
) -> AuthorizeResponse | AuthorizeError:
    return await authorize(data.url, data.code, data.scope)
