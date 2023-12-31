from typing import Optional

from ..context import context
from .interface import IService, IPluginService, INoneBotService


def get_nonebot_service() -> INoneBotService:
    return context.require(INoneBotService)


def create_plugin_service(plugin_name: str) -> IPluginService:
    return get_nonebot_service().create_plugin_service(plugin_name)


def get_plugin_service(
    plugin_name: str, *, raise_on_not_exists: bool = False
) -> Optional[IPluginService]:
    return get_nonebot_service().get_plugin_service(
        plugin_name, raise_on_not_exists=raise_on_not_exists
    )


def get_service_by_qualified_name(
    qualified_name: str, *, raise_on_not_exists: bool = False
) -> Optional[IService]:
    return get_nonebot_service().get_service_by_qualified_name(
        qualified_name, raise_on_not_exists=raise_on_not_exists
    )


__all__ = (
    "get_nonebot_service",
    "create_plugin_service",
    "get_plugin_service",
    "get_service_by_qualified_name",
)
