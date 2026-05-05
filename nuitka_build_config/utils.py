import platform
from typing import TYPE_CHECKING, Literal, Optional

if TYPE_CHECKING:
    from .base import DecoratorMixin
    from .typings import StrList

__all__ = ['set_quotes', 'get_os']


def set_quotes(self: DecoratorMixin, lst: StrList, /) -> StrList:
    quote_marker = self._quote_marker
    use_quotes = self._use_quotes
    output = list()
    for item in lst:
        final_char = '"' if use_quotes else ''
        output.append(item.replace(quote_marker, final_char))
    return output


def get_os() -> Optional[Literal['windows', 'linux', 'macos']]:
    os_name = platform.system().lower()
    match os_name:
        case 'windows' | 'linux': return os_name
        case 'darwin': return 'macos'
        case _: return None
