from abc import ABC, abstractmethod

from nonebot.internal.matcher import Matcher


class IServicePatcher(ABC):
    @abstractmethod
    def patch_matcher(self, matcher: type[Matcher]) -> type[Matcher]:
        raise NotImplementedError()

    @abstractmethod
    def patch_handler(self, retire_on_throw: bool = False):
        raise NotImplementedError()
