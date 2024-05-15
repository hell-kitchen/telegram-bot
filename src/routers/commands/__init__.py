from aiogram import Router
from .base_commands import router as base_commands_router
from .search_command import router as search_cmd_router
from .get_all_command import router as get_all_cmd_router


router = Router(name=__name__)

router.include_routers(
    base_commands_router,
    search_cmd_router,
    get_all_cmd_router,
)

__all__ = (
    "router",
    )
