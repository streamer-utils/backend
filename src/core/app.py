from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.views import routers
from core.config import env_config
from core.db import sessionmanager, DATABASE_URL


@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init(host=DATABASE_URL)

    yield

    await sessionmanager.close()


def start_app() -> FastAPI:
    app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)

    for router in routers:
        app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if env_config.SENTRY_DSN:
        import sentry_sdk
        from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

        sentry_sdk.init(env_config.SENTRY_DSN)

        app.add_middleware(SentryAsgiMiddleware)

    if env_config.ALLOW_HOST:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=env_config.ALLOW_HOST.split(","))
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    return app
