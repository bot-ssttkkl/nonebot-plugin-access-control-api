from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from collections.abc import Generator, Collection

from nonebot import Bot
from nonebot.internal.adapter import Event

from nonebot_plugin_access_control_api.subject import extract_subjects

T_Service = TypeVar("T_Service", bound="IServiceBase", covariant=True)
T_ParentService = TypeVar(
    "T_ParentService", bound=Optional["IServiceBase"], covariant=True
)
T_ChildService = TypeVar("T_ChildService", bound="IServiceBase", covariant=True)


class IServiceBase(Generic[T_Service, T_ParentService, T_ChildService], ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def qualified_name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def parent(self) -> Optional[T_ParentService]:
        raise NotImplementedError()

    @property
    @abstractmethod
    def children(self) -> Collection[T_ChildService]:
        raise NotImplementedError()

    def travel(self) -> Generator[T_Service, None, None]:
        sta = [self]
        while len(sta) != 0:
            top, sta = sta[-1], sta[:-1]
            yield top
            sta.extend(top.children)

    def trace(self) -> Generator[T_Service, None, None]:
        node = self
        while node is not None:
            yield node
            node = node.parent

    def get_child(self, name: str) -> Optional[T_ChildService]:
        for s in self.children:
            if s.name == name:
                return s
        return None

    async def check(
        self,
        bot: Bot,
        event: Event,
        *,
        acquire_rate_limit_token: bool = True,
        throw_on_fail: bool = False,
    ) -> bool:
        subjects = extract_subjects(bot, event)
        return await self.check_by_subject(
            *subjects,
            acquire_rate_limit_token=acquire_rate_limit_token,
            throw_on_fail=throw_on_fail,
        )

    @abstractmethod
    async def check_by_subject(
        self,
        *subjects: str,
        acquire_rate_limit_token: bool = True,
        throw_on_fail: bool = False,
    ) -> bool:
        raise NotImplementedError()

    def __repr__(self):
        return self.qualified_name
