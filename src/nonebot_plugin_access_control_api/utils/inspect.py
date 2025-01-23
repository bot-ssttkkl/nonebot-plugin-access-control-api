import inspect
from typing import Optional

from nonebot import get_loaded_plugins, get_plugin_by_module_name, logger, require


def get_caller_plugin_name() -> Optional[str]:
    """获取当前函数调用者所在的插件名

    尝试自动获取调用者所在的插件名
    """
    frame = inspect.currentframe()
    if frame is None:
        raise ValueError("无法获取当前栈帧")  # pragma: no cover

    while frame := frame.f_back:
        module_name = (module := inspect.getmodule(frame)) and module.__name__
        if not module_name:
            continue

        if module_name.split(".", maxsplit=1)[0] == "nonebot_plugin_access_control_api":
            continue

        plugin = get_plugin_by_module_name(module_name)
        if plugin and plugin.id_ != "nonebot_plugin_access_control_api":
            return plugin.name

    return None  # pragma: no cover

def try_import_impl():
    if "nonebot_plugin_access_control" in get_loaded_plugins():
        return

    if get_caller_plugin_name() == "nonebot_plugin_access_control":
        return

    try:
        require("nonebot_plugin_access_control")
    except RuntimeError as e:
        logger.warning("未安装nonebot-plugin-access-control，权限控制将不会生效")
        logger.debug(e)
