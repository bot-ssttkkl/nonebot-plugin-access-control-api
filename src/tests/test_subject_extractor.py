from typing import Sequence

import pytest
from nonebug import App

from tests.utils.event import SELF_ID, fake_ob11_group_message_event


@pytest.mark.asyncio
async def test_subject_extractor(app: App):
    from nonebot.internal.adapter import Event
    from nonebot.adapters.onebot.v11 import Bot as OB11Bot

    from nonebot_plugin_access_control_api.subject.model import SubjectModel
    from nonebot_plugin_access_control_api.subject.manager import SubjectManager
    from nonebot_plugin_access_control_api.subject import (
        extract_subjects,
        add_subject_extractor,
    )

    @add_subject_extractor
    def extractor_head():
        return [SubjectModel("head", "extractor_head", "head")]

    @add_subject_extractor
    def extractor_a(event: Event, manager: SubjectManager):
        manager.append(SubjectModel(event.get_event_name(), "extractor_a", "eventname"))

    @add_subject_extractor
    def extractor_b(event: Event, manager: SubjectManager):
        manager.insert_before(
            "eventname", SubjectModel(event.get_user_id(), "extractor_b", "userid")
        )

    @add_subject_extractor
    def extractor_tail(current: Sequence[SubjectModel]):
        return [*current, SubjectModel("tail", "extractor_tail", "tail")]

    async with app.test_api() as ctx:
        bot = ctx.create_bot(base=OB11Bot, self_id=str(SELF_ID))
        event = fake_ob11_group_message_event("test", user_id=23456)
        subjects = extract_subjects(bot, event)
        assert subjects == ["head", "23456", "message.group", "tail"]
