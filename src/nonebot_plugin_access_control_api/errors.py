from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models.rate_limit import AcquireTokenResult


class AccessControlError(RuntimeError): ...


class PermissionDeniedError(AccessControlError): ...


class RateLimitedError(AccessControlError):
    def __init__(self, result: "AcquireTokenResult"):
        self.result = result


class AccessControlBadRequestError(AccessControlError): ...


class AccessControlQueryError(AccessControlError): ...
