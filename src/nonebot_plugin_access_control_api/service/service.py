from abc import ABC
from datetime import timedelta
from typing import Generic, TypeVar, Optional, AsyncGenerator

from nonebot import Bot
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher

from ..context import context
from .interface import IService
from ..event_bus import T_Listener
from ..models.permission import Permission
from .interface.factory import IServiceComponentFactory
from ..errors import RateLimitedError, AccessControlError, PermissionDeniedError
from ..models.rate_limit import RateLimitRule, IRateLimitToken, AcquireTokenResult

T_ParentService = TypeVar("T_ParentService", bound=Optional["Service"], covariant=True)
T_ChildService = TypeVar("T_ChildService", bound="Service", covariant=True)


class Service(
    Generic[T_ParentService, T_ChildService],
    IService["Service", T_ParentService, T_ChildService],
    ABC,
):
    def __init__(self):
        factory = context.require(IServiceComponentFactory)
        self._patcher_impl = factory.create_patcher_impl(self)
        self._permission_impl = factory.create_permission_impl(self)
        self._rate_limit_impl = factory.create_rate_limit_impl(self)

    def patch_matcher(self, matcher: type[Matcher]) -> type[Matcher]:
        return self._patcher_impl.patch_matcher(matcher)

    def patch_handler(self, retire_on_throw: bool = False):
        return self._patcher_impl.patch_handler(retire_on_throw)

    async def check_by_subject(
        self,
        *subjects: str,
        acquire_rate_limit_token: bool = True,
        throw_on_fail: bool = False,
    ) -> bool:
        if not throw_on_fail:
            try:
                await self.check_by_subject(
                    *subjects,
                    acquire_rate_limit_token=acquire_rate_limit_token,
                    throw_on_fail=True,
                )
                return True
            except AccessControlError:
                return False

        allow = await self.check_permission(*subjects)
        if not allow:
            raise PermissionDeniedError()

        if acquire_rate_limit_token:
            result = (
                await self.acquire_token_for_rate_limit_by_subjects_receiving_result(
                    *subjects
                )
            )
            if not result.success:
                raise RateLimitedError(result)

    def on_set_permission(self, func: Optional[T_Listener] = None):
        return self._permission_impl.on_set_permission(func)

    def on_change_permission(self, func: Optional[T_Listener] = None):
        return self._permission_impl.on_change_permission(func)

    def on_remove_permission(self, func: Optional[T_Listener] = None):
        return self._permission_impl.on_remove_permission(func)

    async def get_permission_by_subject(
        self, *subject: str, trace: bool = True
    ) -> Optional[Permission]:
        return await self._permission_impl.get_permission_by_subject(
            *subject, trace=trace
        )

    def get_permissions(
        self, *, trace: bool = True
    ) -> AsyncGenerator[Permission, None]:
        return self._permission_impl.get_permissions(trace=trace)

    @classmethod
    def get_all_permissions_by_subject(
        cls, *subject: str
    ) -> AsyncGenerator[Permission, None]:
        factory = context.require(IServiceComponentFactory)
        return factory.typeof_permission_impl().get_all_permissions_by_subject(*subject)

    @classmethod
    def get_all_permissions(cls) -> AsyncGenerator[Permission, None]:
        factory = context.require(IServiceComponentFactory)
        return factory.typeof_permission_impl().get_all_permissions()

    async def set_permission(self, subject: str, allow: bool) -> bool:
        return await self._permission_impl.set_permission(subject, allow)

    async def remove_permission(self, subject: str) -> bool:
        return await self._permission_impl.remove_permission(subject)

    async def check_permission(self, *subject: str) -> bool:
        return await self._permission_impl.check_permission(*subject)

    def on_add_rate_limit_rule(self, func: Optional[T_Listener] = None):
        return self._rate_limit_impl.on_add_rate_limit_rule(func)

    def on_remove_rate_limit_rule(self, func: Optional[T_Listener] = None):
        return self._rate_limit_impl.on_remove_rate_limit_rule(func)

    def get_rate_limit_rules_by_subject(
        self, *subject: str, trace: bool = True
    ) -> AsyncGenerator[RateLimitRule, None]:
        return self._rate_limit_impl.get_rate_limit_rules_by_subject(
            *subject, trace=trace
        )

    def get_rate_limit_rules(
        self, *, trace: bool = True
    ) -> AsyncGenerator[RateLimitRule, None]:
        return self._rate_limit_impl.get_rate_limit_rules(trace=trace)

    @classmethod
    def get_all_rate_limit_rules_by_subject(
        cls, *subject: str
    ) -> AsyncGenerator[RateLimitRule, None]:
        factory = context.require(IServiceComponentFactory)
        return factory.typeof_rate_limit_impl().get_all_rate_limit_rules_by_subject(
            *subject
        )

    @classmethod
    def get_all_rate_limit_rules(cls) -> AsyncGenerator[RateLimitRule, None]:
        factory = context.require(IServiceComponentFactory)
        return factory.typeof_rate_limit_impl().get_all_rate_limit_rules()

    async def add_rate_limit_rule(
        self, subject: str, time_span: timedelta, limit: int, overwrite: bool = False
    ) -> RateLimitRule:
        return await self._rate_limit_impl.add_rate_limit_rule(
            subject, time_span, limit, overwrite
        )

    @classmethod
    async def remove_rate_limit_rule(cls, rule_id: str) -> bool:
        factory = context.require(IServiceComponentFactory)
        return await factory.typeof_rate_limit_impl().remove_rate_limit_rule(rule_id)

    async def acquire_token_for_rate_limit(
        self, bot: Bot, event: Event
    ) -> Optional[IRateLimitToken]:
        return await self._rate_limit_impl.acquire_token_for_rate_limit(bot, event)

    async def acquire_token_for_rate_limit_receiving_result(
        self, bot: Bot, event: Event
    ) -> AcquireTokenResult:
        return (
            await self._rate_limit_impl.acquire_token_for_rate_limit_receiving_result(
                bot, event
            )
        )

    async def acquire_token_for_rate_limit_by_subjects(
        self, *subject: str
    ) -> Optional[IRateLimitToken]:
        return await self._rate_limit_impl.acquire_token_for_rate_limit_by_subjects(
            *subject
        )

    async def acquire_token_for_rate_limit_by_subjects_receiving_result(
        self, *subject: str
    ) -> AcquireTokenResult:
        return await self._rate_limit_impl.acquire_token_for_rate_limit_by_subjects_receiving_result(
            *subject
        )

    @classmethod
    async def clear_rate_limit_tokens(cls):
        factory = context.require(IServiceComponentFactory)
        return await factory.typeof_rate_limit_impl().clear_rate_limit_tokens()
