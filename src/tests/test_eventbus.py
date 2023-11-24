from typing import Optional

import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_eventbus(app: App):
    from nonebot_plugin_access_control_api.models.permission import Permission
    from nonebot_plugin_access_control_api.service import Service, get_nonebot_service
    from nonebot_plugin_access_control_api.event_bus import (
        EventType,
        on_event,
        fire_event,
    )

    received_event_params: Optional[dict] = None

    @on_event(EventType.service_set_permission, lambda: True)
    def event_handler(service: Service, permission: Permission):
        nonlocal received_event_params
        received_event_params = {"service": service, "permission": permission}

    event_params = {
        "service": get_nonebot_service(),
        "permission": Permission(get_nonebot_service(), "all", True),
    }
    await fire_event(EventType.service_set_permission, event_params)
    assert received_event_params == event_params
