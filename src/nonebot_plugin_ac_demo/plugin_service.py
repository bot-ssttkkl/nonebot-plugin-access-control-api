from nonebot import require

require("nonebot_plugin_access_control_api")

from nonebot_plugin_access_control_api.service import create_plugin_service

plugin_service = create_plugin_service("nonebot_plugin_ac_demo")