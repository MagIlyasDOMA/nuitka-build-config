import dataclasses
from functools import wraps
from typing import Any
from .typings import ArgvAddFunc, StrList
from .typings.models import BaseOSParamsDict
from .utils import set_quotes

__all__ = ['argv_add', 'dataclass', 'os_params']


def argv_add(method: ArgvAddFunc) -> ArgvAddFunc:
    @wraps(method)
    def new_method(self, argv: StrList, arg: Any) -> StrList:
        data = set_quotes(self, method(self, argv, arg))
        argv.extend(data)
        return data
    return new_method


dataclass = dataclasses.dataclass(slots=True, frozen=True, kw_only=True)


def os_params(method: ArgvAddFunc) -> ArgvAddFunc:
    @wraps(method)
    @argv_add
    def new_method(self, argv: StrList, arg: BaseOSParamsDict) -> StrList:
        data = method(self, argv, arg)
        data.extend(arg.get('extra_flags', []))
        return data
    return new_method
