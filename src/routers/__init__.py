from aiogram import Router
from .commands import rt as commands_router
from .common import rt as common_router

__all__ = (
    "rt",
)

rt = Router(name=__name__)
rt.include_routers(
    commands_router,
    common_router,
)