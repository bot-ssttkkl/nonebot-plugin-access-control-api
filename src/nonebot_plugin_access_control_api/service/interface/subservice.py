from abc import ABC
from typing import Generic, TypeVar, Optional

from .service import IService
from .subservice_owner import ISubServiceOwner

T_Service = TypeVar("T_Service", bound=IService, covariant=True)
T_ParentService = TypeVar("T_ParentService", bound=Optional[IService], covariant=True)
T_ChildService = TypeVar("T_ChildService", bound="ISubService", covariant=True)


class ISubService(
    Generic[T_Service, T_ParentService, T_ChildService],
    IService[T_Service, T_ParentService, T_ChildService],
    ISubServiceOwner[T_ChildService],
    ABC,
):
    ...
