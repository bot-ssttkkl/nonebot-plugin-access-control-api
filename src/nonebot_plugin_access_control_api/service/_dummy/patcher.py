from functools import wraps

from nonebot.internal.matcher import Matcher

from ..interface import IService
from ..interface.patcher import IServicePatcher


class ServicePatcherImpl(IServicePatcher):
    def __init__(self, service: IService):
        self.service = service

    def patch_matcher(self, matcher: type[Matcher]) -> type[Matcher]:
        return matcher

    def patch_handler(self, retire_on_throw: bool = False):
        def decorator(func):
            @wraps(func)
            async def wrapped_func(*args, **kwargs):
                return await func(*args, **kwargs)

            return wrapped_func

        return decorator
