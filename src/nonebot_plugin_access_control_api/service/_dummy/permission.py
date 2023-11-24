from typing import Optional
from collections.abc import AsyncGenerator

from nonebot_plugin_access_control_api.models.permission import Permission
from nonebot_plugin_access_control_api.service.interface.service import IService
from nonebot_plugin_access_control_api.event_bus import EventType, T_Listener, on_event
from nonebot_plugin_access_control_api.service.interface.permission import (
    IServicePermission,
)


class ServicePermissionImpl(IServicePermission):
    def __init__(self, service: IService):
        self.service = service

    def on_set_permission(self, func: Optional[T_Listener] = None):
        return on_event(
            EventType.service_set_permission,
            lambda service: service == self.service,
            func,
        )

    def on_change_permission(self, func: Optional[T_Listener] = None):
        return on_event(
            EventType.service_change_permission,
            lambda service: service == self.service,
            func,
        )

    def on_remove_permission(self, func: Optional[T_Listener] = None):
        return on_event(
            EventType.service_remove_permission,
            lambda service: service == self.service,
            func,
        )

    async def get_permission_by_subject(
        self, *subject: str, trace: bool = True
    ) -> Optional[Permission]:
        return
        yield None  # noqa

    async def get_permissions(
        self, *, trace: bool = True
    ) -> AsyncGenerator[Permission, None]:
        return
        yield None  # noqa

    @classmethod
    async def get_all_permissions_by_subject(
        cls, *subject: str
    ) -> AsyncGenerator[Permission, None]:
        return
        yield None  # noqa

    @classmethod
    async def get_all_permissions(cls) -> AsyncGenerator[Permission, None]:
        return
        yield None  # noqa

    async def set_permission(self, subject: str, allow: bool) -> bool:
        raise NotImplementedError()

    async def remove_permission(self, subject: str) -> bool:
        raise NotImplementedError()

    async def check_permission(self, *subject: str) -> bool:
        return True
