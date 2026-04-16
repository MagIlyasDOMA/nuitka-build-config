from typing import Any
from .typings import ArgvAddFunc, StrList


def argv_add(method: ArgvAddFunc) -> ArgvAddFunc:
    def new_method(self, argv: StrList, arg: Any) -> StrList:
        data = method(self, argv, arg)
        argv.extend(data)
        return data
    new_method.argv_add = True
    new_method.config_attr_type = 'argv_add'
    return new_method
