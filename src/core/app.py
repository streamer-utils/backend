from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from core.config import env_config


def start_app() -> FastAPI:
    app = FastAPI(default_response_class=ORJSONResponse)

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
