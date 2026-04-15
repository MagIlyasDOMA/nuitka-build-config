from typing import Any, Optional, Union, Callable
from .typings import *


class ArgvAddMethod:
    _custom: Optional[Callable]

    def __set_name__(self, owner, name: str):
        self.__name__ = name

    def __init__(self, field_type: FieldType, field_name: NullStr = None,
                 cli: bool = True, flag: NullStr = None,
                 type_data: Optional[Union[dict]] = None):
        self.field_type = field_type
        self.field_name = field_name or self.__name__.lstrip('_add_')
        self.cli = cli
        self.flag = flag or f"--{self.field_name.replace('_', '-')}"
        self.type_data = type_data

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
            case 'strlist': return arg
            case 'filelist': return list(map(lambda path: str(path), arg))
            case 'custom': return self._custom(argv, arg)
        return []

    @classmethod
    def custom_getter(cls, func):
        return cls()
