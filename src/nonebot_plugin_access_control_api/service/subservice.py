from typing import TYPE_CHECKING, Union

from .service import Service
from .interface import ISubService
from .subservice_owner import SubServiceOwner

if TYPE_CHECKING:
    from .plugin_service import PluginService


class SubService(
    SubServiceOwner[Service, Union["PluginService", "SubService"], "SubService"],
    Service["NoneBotService", "SubService"],
    ISubService[Service, Union["PluginService", "SubService"], "SubService"],
):
    def __init__(self, name: str, parent: Union["PluginService", "SubService"]):
        super().__init__()
        self._name = name
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def qualified_name(self) -> str:
        return self.parent.qualified_name + "." + self.name

    @property
    def parent(self) -> Union["PluginService", "SubService"]:
        return self._parent

    def _make_subservice(self, name: str) -> "SubService":
        return SubService(name, self)
