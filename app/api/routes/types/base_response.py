from typing import TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class GenericResponse(GenericModel, Generic[T]):
    data: T
    status_code: int
