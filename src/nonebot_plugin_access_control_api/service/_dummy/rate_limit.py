from typing import Optional
from datetime import timedelta
from collections.abc import AsyncGenerator

from nonebot_plugin_access_control_api.service.interface import IService
from nonebot_plugin_access_control_api.event_bus import EventType, T_Listener, on_event
from nonebot_plugin_access_control_api.service.interface.rate_limit import (
    IServiceRateLimit,
)
from nonebot_plugin_access_control_api.models.rate_limit import (
    RateLimitRule,
    IRateLimitToken,
    AcquireTokenResult,
)


class RateLimitTokenImpl(IRateLimitToken):
    async def retire(self):
        pass


class ServiceRateLimitImpl(IServiceRateLimit):
    def __init__(self, service: IService):
        self.service = service

    def on_add_rate_limit_rule(self, func: Optional[T_Listener] = None):
        return on_event(
            EventType.service_add_rate_limit_rule,
            lambda service: service == self.service,
            func,
        )

    def on_remove_rate_limit_rule(self, func: Optional[T_Listener] = None):
        return on_event(
            EventType.service_remove_rate_limit_rule,
            lambda service: service == self.service,
            func,
        )

    async def get_rate_limit_rules_by_subject(
        self, *subject: str, trace: bool = True
    ) -> AsyncGenerator[RateLimitRule, None]:
        return
        yield None  # noqa

    async def get_rate_limit_rules(
        self, *, trace: bool = True
    ) -> AsyncGenerator[RateLimitRule, None]:
        return
        yield None  # noqa

    @classmethod
    async def get_all_rate_limit_rules_by_subject(
        cls, *subject: str
    ) -> AsyncGenerator[RateLimitRule, None]:
        return
        yield None  # noqa

    @classmethod
    async def get_all_rate_limit_rules(cls) -> AsyncGenerator[RateLimitRule, None]:
        return
        yield None  # noqa

    async def add_rate_limit_rule(
        self, subject: str, time_span: timedelta, limit: int, overwrite: bool = False
    ) -> RateLimitRule:
        raise NotImplementedError()

    @classmethod
    async def remove_rate_limit_rule(cls, rule_id: str) -> bool:
        raise NotImplementedError()

    async def acquire_token_for_rate_limit_by_subjects_receiving_result(
        self, *subject: str
    ) -> AcquireTokenResult:
        return AcquireTokenResult(success=True, token=RateLimitTokenImpl())

    @classmethod
    async def clear_rate_limit_tokens(cls):
        pass
