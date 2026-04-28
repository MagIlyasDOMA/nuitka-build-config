import dataclasses
from typing import Any, TYPE_CHECKING
from .typings import ArgvAddFunc, StrList

if TYPE_CHECKING:
    from .base import DecoratorMixin

__all__ = ['argv_add', 'dataclass']


def set_quotes(self: DecoratorMixin, lst: StrList, /) -> StrList:
    quote_marker = self._quote_marker
    use_quotes = self._use_quotes
    output = list()
    for item in lst:
        final_char = '"' if use_quotes else ''
        output.append(item.replace(quote_marker, final_char))
    return output


def argv_add(method: ArgvAddFunc) -> ArgvAddFunc:
    def new_method(self, argv: StrList, arg: Any) -> StrList:
        data = set_quotes(self, method(self, argv, arg))
        argv.extend(data)
        return data
    new_method.argv_add = True
    new_method.config_attr_type = 'argv_add'
    return new_method


dataclass = dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
