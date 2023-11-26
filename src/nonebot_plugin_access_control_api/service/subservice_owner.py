import re
from abc import ABC, abstractmethod
from collections.abc import Collection
from typing import Generic, TypeVar, Optional

from nonebot import logger

from ..errors import AccessControlError
from .interface import IService, ISubServiceOwner


def _validate_name(name: str) -> bool:
    match_result = re.match(r"[_a-zA-Z]\w*", name)
    return match_result is not None


T_Service = TypeVar("T_Service", bound=IService, covariant=True)
T_ParentService = TypeVar("T_ParentService", bound=Optional[IService], covariant=True)
T_ChildService = TypeVar("T_ChildService", bound="SubServiceOwner", covariant=True)


class SubServiceOwner(
    Generic[T_Service, T_ParentService, T_ChildService],
    IService[T_Service, T_ParentService, T_ChildService],
    ISubServiceOwner[T_ChildService],
    ABC,
):
    def __init__(self):
        super().__init__()
        self._subservices: dict[str, T_ChildService] = {}

    @abstractmethod
    def _make_subservice(self, name: str) -> T_ChildService:
        raise NotImplementedError()

    @property
    def children(self) -> Collection[T_ChildService]:
        return self._subservices.values()

    def create_subservice(self, name: str) -> T_ChildService:
        if not _validate_name(name):
            raise AccessControlError(f"invalid name: {name}")

        if name in self._subservices:
            raise AccessControlError(
                f"subservice already exists: {self.qualified_name}.{name}"
            )

        service = self._make_subservice(name)
        self._subservices[name] = service
        logger.trace(
            f"created subservice {service.qualified_name}"
            f"  (parent: {self.qualified_name})"
        )
        return self._subservices[name]
