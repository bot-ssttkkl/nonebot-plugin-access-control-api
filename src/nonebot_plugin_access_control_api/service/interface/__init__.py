from .service import IService
from .subservice import ISubService
from .plugin_service import IPluginService
from .nonebot_service import INoneBotService
from .subservice_owner import ISubServiceOwner

__all__ = (
    "IService",
    "INoneBotService",
    "IPluginService",
    "ISubService",
    "ISubServiceOwner",
)
