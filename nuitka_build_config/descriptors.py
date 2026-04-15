import functools
from typing import Any, Optional, Union
from .typings import *


class ArgvAddMethod:
    def __set_name__(self, owner, name: str):
        self.__name__ = name

    def __init__(self, field_type: FieldType = 'str', field_name: NullStr = None,
                 cli: bool = True, flag: NullStr = None, prefix: str = '_add_',
                 type_data: Optional[Union[dict]] = None, choices: Optional[StrList] = None):
        self.field_type = field_type
        self.field_name = field_name or self.__name__.lstrip(prefix)
        self.cli = cli
        self.flag = flag or f"--{self.field_name.replace('_', '-')}"
        self.type_data = type_data
        self.choices = choices or []
        if field_type == 'choice': self.choices.extend(type_data.keys())
        self._custom = lambda argv, arg: []

    def __call__(self, argv: StrList, arg: Any) -> StrList:
        match self.field_type:
            case 'str': return [f'{self.flag}={arg}']
            case 'int':
                if not isinstance(arg, int):
                    raise TypeError("Argument must be an integer")
                return [f'{self.flag}={arg}']
            case 'bool': return [self.flag] if arg else []
            case 'ternary':
                if arg is None: return []
                return [self.type_data[str(bool(arg)).lower()]]
            case 'choice': return self.type_data[arg]
            case 'strlist' | 'filelist': return [f'{self.flag}={el}' for el in arg]
            case 'custom': return self._custom(argv, arg)
        return []

    @classmethod
    def custom_getter(cls, field_name: NullStr = None, prefix: str = '_add_',
                      cli: bool = True, flag: NullStr = None,
                      type_data: Optional[Union[dict]] = None):
        def decorator(func):
            self = cls('custom', field_name or func.__name__.lstrip(prefix),
                       cli, flag, prefix, type_data)
            functools.wraps(func)(self)
            self._custom = func
            return self
        return decorator

