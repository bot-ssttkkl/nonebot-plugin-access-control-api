import pytest
import pytest_asyncio
from nonebug import NONEBOT_INIT_KWARGS, App


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "log_level": "DEBUG",
    }


@pytest_asyncio.fixture(autouse=True)
async def prepare_nonebot(app: App):
    import nonebot
    from nonebot.adapters.onebot.v11 import Adapter

    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)

    nonebot.require("nonebot_plugin_access_control_api")
    nonebot.require("nonebot_plugin_ac_demo")

    yield app
