from .auth import auth_router


routers = [
    auth_router
]

__all__ = ['routers']
