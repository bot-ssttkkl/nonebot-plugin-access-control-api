from typing import Protocol

from . import IService
from .patcher import IServicePatcher
from .rate_limit import IServiceRateLimit
from .permission import IServicePermission


class IServiceComponentFactory(Protocol):
    def create_patcher_impl(self, service: IService) -> IServicePatcher:
        ...

    def typeof_patcher_impl(self) -> type[IServicePatcher]:
        ...

    def create_permission_impl(self, service: IService) -> IServicePermission:
        ...

    def typeof_permission_impl(self) -> type[IServicePermission]:
        ...

    def create_rate_limit_impl(self, service: IService) -> IServiceRateLimit:
        ...

    def typeof_rate_limit_impl(self) -> type[IServiceRateLimit]:
        ...
