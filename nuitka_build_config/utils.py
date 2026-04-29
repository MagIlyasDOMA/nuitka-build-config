from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import DecoratorMixin
    from .typings import StrList

__all__ = ['set_quotes']


def set_quotes(self: DecoratorMixin, lst: StrList, /) -> StrList:
    quote_marker = self._quote_marker
    use_quotes = self._use_quotes
    output = list()
    for item in lst:
        final_char = '"' if use_quotes else ''
        output.append(item.replace(quote_marker, final_char))
    return output
