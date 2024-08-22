from pydantic import BaseModel


class GetAuthorizeLinkResponse(BaseModel):
    url: str


class AuthorizeData(BaseModel):
    url: str
    code: str
    scope: list[str]


class AuthorizeResponse(BaseModel):
    token: str
    # refresh_token: str


class AuthorizeError(BaseModel):
    error: str
