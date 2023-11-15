from collections.abc import AsyncGenerator
from datetime import timedelta
from typing import Generic, TypeVar, Optional, Collection, Generator

from nonebot import Bot
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher

from .interface import IService
from ..event_bus import T_Listener
from ..models.permission import Permission
from ..models.rate_limit import RateLimitRule, IRateLimitToken, AcquireTokenResult

T_Service = TypeVar("T_Service", bound="IService", covariant=True)
T_ParentService = TypeVar(
    "T_ParentService", bound=Optional["IService"], covariant=True
)
T_ChildService = TypeVar("T_ChildService", bound="IService", covariant=True)


class DelegateService(Generic[T_Service, T_ParentService, T_ChildService],
                      IService[T_Service, T_ParentService, T_ChildService]):
    _delegate: Optional[IService[T_Service, T_ParentService, T_ChildService]] = None

    def __init__(self):
        self._delegate = None

    def _set_delegate(self, delegate: Optional[IService[T_Service, T_ParentService, T_ChildService]]):
        self._delegate = delegate

    @classmethod
    def _delegate_cls(cls) -> Optional[type[IService[T_Service, T_ParentService, T_ChildService]]]:
        return None

    @property
    def name(self) -> str:
        return self._delegate.name

    @property
    def qualified_name(self) -> str:
        return self._delegate.qualified_name

    @property
    def parent(self) -> Optional[T_ParentService]:
        return self._delegate.parent

    @property
    def children(self) -> Collection[T_ChildService]:
        return self._delegate.children

    def travel(self) -> Generator[T_Service, None, None]:
        yield from self._delegate.travel()

    def trace(self) -> Generator[T_Service, None, None]:
        yield from self._delegate.trace()

    def get_child(self, name: str) -> Optional[T_ChildService]:
        return self._delegate.get_child(name)

    def patch_matcher(self, matcher: type[Matcher]) -> type[Matcher]:
        return self._delegate.patch_matcher(matcher)

    def patch_handler(self, retire_on_throw: bool = False):
        return self._delegate.patch_handler(retire_on_throw)

    async def check(
            self, bot: Bot,
            event: Event,
            *,
            acquire_rate_limit_token: bool = True,
            throw_on_fail: bool = False,
    ) -> bool:
        return await self._delegate.check(
            bot, event,
            acquire_rate_limit_token=acquire_rate_limit_token,
            throw_on_fail=throw_on_fail
        )

    async def check_by_subject(
            self,
            *subjects: str,
            acquire_rate_limit_token: bool = True,
            throw_on_fail: bool = False,
    ) -> bool:
        return await self._delegate.check_by_subject(
            *subjects,
            acquire_rate_limit_token=acquire_rate_limit_token,
            throw_on_fail=throw_on_fail
        )

    def on_set_permission(self, func: Optional[T_Listener] = None):
        return self._delegate.on_set_permission(func)

    def on_change_permission(self, func: Optional[T_Listener] = None):
        return self._delegate.on_change_permission(func)

    def on_remove_permission(self, func: Optional[T_Listener] = None):
        return self._delegate.on_remove_permission(func)

    async def get_permission_by_subject(
            self, *subject: str, trace: bool = True
    ) -> Optional[Permission]:
        return await self._delegate.get_permission_by_subject(*subject, trace=trace)

    def get_permissions(
            self, *, trace: bool = True
    ) -> AsyncGenerator[Permission, None]:
        return self._delegate.get_permissions(trace=trace)

    @classmethod
    def get_all_permissions_by_subject(
            cls, *subject: str
    ) -> AsyncGenerator[Permission, None]:
        return cls._delegate_cls().get_all_permissions_by_subject(*subject)

    @classmethod
    def get_all_permissions(cls) -> AsyncGenerator[Permission, None]:
        return cls._delegate_cls().get_all_permissions()

    async def set_permission(self, subject: str, allow: bool) -> bool:
        return await self._delegate.set_permission(subject, allow)

    async def remove_permission(self, subject: str) -> bool:
        return await self._delegate.remove_permission(subject)

    async def check_permission(self, *subject: str) -> bool:
        return await self._delegate.check_permission(*subject)

    def on_add_rate_limit_rule(self, func: Optional[T_Listener] = None):
        return self._delegate.on_add_rate_limit_rule(func)

    def on_remove_rate_limit_rule(self, func: Optional[T_Listener] = None):
        return self._delegate.on_remove_rate_limit_rule(func)

    def get_rate_limit_rules_by_subject(
            self, *subject: str, trace: bool = True
    ) -> AsyncGenerator[RateLimitRule, None]:
        return self._delegate.get_rate_limit_rules_by_subject(*subject, trace=trace)

    def get_rate_limit_rules(
            self, *, trace: bool = True
    ) -> AsyncGenerator[RateLimitRule, None]:
        return self._delegate.get_rate_limit_rules(trace=trace)

    @classmethod
    def get_all_rate_limit_rules_by_subject(
            cls, *subject: str
    ) -> AsyncGenerator[RateLimitRule, None]:
        return cls._delegate_cls().get_all_rate_limit_rules_by_subject(*subject)

    @classmethod
    def get_all_rate_limit_rules(cls) -> AsyncGenerator[RateLimitRule, None]:
        return cls._delegate_cls().get_all_rate_limit_rules()

    async def add_rate_limit_rule(
            self, subject: str, time_span: timedelta, limit: int, overwrite: bool = False
    ) -> RateLimitRule:
        return await self._delegate.add_rate_limit_rule(subject, time_span, limit, overwrite)

    @classmethod
    async def remove_rate_limit_rule(cls, rule_id: str) -> bool:
        return await cls._delegate_cls().remove_rate_limit_rule(rule_id)

    async def acquire_token_for_rate_limit(
            self, bot: Bot, event: Event
    ) -> Optional[IRateLimitToken]:
        return await self._delegate.acquire_token_for_rate_limit(bot, event)

    async def acquire_token_for_rate_limit_receiving_result(
            self, bot: Bot, event: Event
    ) -> AcquireTokenResult:
        return await self._delegate.acquire_token_for_rate_limit_receiving_result(bot, event)

    async def acquire_token_for_rate_limit_by_subjects(
            self, *subject: str
    ) -> Optional[IRateLimitToken]:
        return await self._delegate.acquire_token_for_rate_limit_by_subjects(*subject)

    async def acquire_token_for_rate_limit_by_subjects_receiving_result(
            self, *subject: str
    ) -> AcquireTokenResult:
        return await self._delegate.acquire_token_for_rate_limit_by_subjects_receiving_result(*subject)

    @classmethod
    async def clear_rate_limit_tokens(cls):
        return await cls._delegate_cls().clear_rate_limit_tokens()
