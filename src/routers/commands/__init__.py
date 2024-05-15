from aiogram import Router
from .base_commands import rt as base_commands_router
from .search_command import rt as search_cmd_router
from .get_all_command import rt as get_all_cmd_router

__all__ = (
    "rt",
    )

rt = Router(name=__name__)

rt.include_routers(
    base_commands_router,
    search_cmd_router,
    get_all_cmd_router,
)