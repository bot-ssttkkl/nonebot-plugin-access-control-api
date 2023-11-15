"""
nonebot-plugin-access-control-api

@Author         : ssttkkl
@License        : MIT
@GitHub         : https://github.com/bot-ssttkkl/nonebot-access-control-api
"""
from nonebot import require

require("nonebot_plugin_session")
require("ssttkkl_nonebot_utils")

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="权限控制API",
    description="为插件开发者提供适配nonebot-plugin-access-control的API",
    usage="参考 https://github.com/bot-ssttkkl/nonebot-plugin-access-control-api",
    type="library",
    homepage="https://github.com/bot-ssttkkl/nonebot-plugin-access-control-api",
)

from . import service  # noqa
