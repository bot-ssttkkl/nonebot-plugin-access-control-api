from typing import Optional
from collections.abc import Collection

import nonebot
from nonebot import logger

from .service import Service
from ..context import context
from .interface import IService
from .plugin_service import PluginService
from .interface.nonebot_service import INoneBotService
from ..errors import AccessControlError, AccessControlQueryError


@context.bind_singleton_to(INoneBotService)
class NoneBotService(
    Service[None, PluginService], INoneBotService[Service, PluginService]
):
    def __init__(self):
        super().__init__()
        self._plugin_services: dict[str, PluginService] = {}

    @property
    def name(self) -> str:
        return "nonebot"

    @property
    def qualified_name(self) -> str:
        return "nonebot"

    @property
    def parent(self) -> None:
        return None

    @property
    def children(self) -> Collection[PluginService]:
        return self._plugin_services.values()

    def _create_plugin_service(
        self, plugin_name: str, auto_create: bool
    ) -> PluginService:
        if plugin_name in self._plugin_services:
            raise ValueError(f"{plugin_name} already created")

        service = PluginService(plugin_name, auto_create, self)
        self._plugin_services[plugin_name] = service
        logger.trace(f"created plugin service {service.qualified_name}")
        return service

    def create_plugin_service(self, plugin_name: str) -> PluginService:
        return self._create_plugin_service(plugin_name, auto_create=False)

    def get_plugin_service(
        self, plugin_name: str, *, raise_on_not_exists: bool = False
    ) -> Optional[PluginService]:
        if plugin_name in self._plugin_services:
            return self._plugin_services[plugin_name]
        if raise_on_not_exists:
            raise AccessControlQueryError(f"找不到服务 {plugin_name}")
        return None

    def get_or_create_plugin_service(self, plugin_name: str) -> PluginService:
        if plugin_name in self._plugin_services:
            return self._plugin_services[plugin_name]
        else:
            plugin = nonebot.get_plugin(plugin_name)
            if plugin is not None:
                return self._create_plugin_service(plugin_name, auto_create=True)
            else:
                raise AccessControlError("No such plugin")

    def get_service_by_qualified_name(
        self, qualified_name: str, *, raise_on_not_exists: bool = False
    ) -> Optional[IService]:
        if qualified_name == "nonebot":
            return self

        seg = qualified_name.split(".")
        service: Optional[IService] = self.get_plugin_service(seg[0])
        for i in range(1, len(seg)):
            if service is None:
                if raise_on_not_exists:
                    raise AccessControlQueryError(f"找不到服务 {qualified_name}")
                return None
            service = service.get_child(seg[i])
        return service
