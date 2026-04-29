import dataclasses
from typing import Any
from .typings import ArgvAddFunc, StrList
from .utils import set_quotes

__all__ = ['argv_add', 'dataclass']


def argv_add(method: ArgvAddFunc) -> ArgvAddFunc:
    def new_method(self, argv: StrList, arg: Any) -> StrList:
        data = set_quotes(self, method(self, argv, arg))
        argv.extend(data)
        return data
    new_method.argv_add = True
    new_method.config_attr_type = 'argv_add'
    return new_method


dataclass = dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
