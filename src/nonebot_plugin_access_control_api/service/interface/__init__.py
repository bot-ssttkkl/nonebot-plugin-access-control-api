from .nonebot_service import INoneBotService
from .plugin_service import IPluginService
from .service import IService
from .subservice import ISubService
from .subservice_owner import ISubServiceOwner

__all__ = (
    "IService",
    "INoneBotService",
    "IPluginService",
    "ISubService",
    "ISubServiceOwner",
)
