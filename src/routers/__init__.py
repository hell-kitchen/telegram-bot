__all__ = ("rt", )

from aiogram import Router
from .commands import rt as commands_router
from .common import rt as common_router

rt = Router(name=__name__)
rt.include_routers(
    commands_router,
    common_router,
)