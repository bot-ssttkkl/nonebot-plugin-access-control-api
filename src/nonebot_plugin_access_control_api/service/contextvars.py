from contextvars import ContextVar

current_rate_limit_token = ContextVar("accctrl_current_token")
"""
仅当为事件处理函数上应用装饰器`Service.patch_handle()`时有效。

在事件处理函数中能够获取到当前限流token，用于收回限流消耗的次数。
"""

__all__ = ("current_rate_limit_token",)
