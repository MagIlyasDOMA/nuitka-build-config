from typing import Literal, Optional, List, Union, Callable
from pathlike_typing import PathLike

__all__ = ['BinFileType', 'PythonFlagType', 'NullStr', 'StrList', 'ArgType', 'ArgvAddMethod', 'ArgvAddStrMethod']

BinFileType = Literal['accelerated', 'onefile', 'standalone', 'module', 'app', 'app-dist', 'package', 'dll']
PythonFlagType = Literal['-S', 'no_site', '-O', 'no_asserts', 'no_warnings', 'no_docstrings', '-u', 'unbuffered']
NullStr = Optional[str]
StrList = List[str]
ArgType = Union[str, bool, PathLike]
ArgvAddMethod = Callable[['NuitkaBuilder', StrList, ArgType], StrList]
ArgvAddStrMethod = Callable[['NuitkaBuilder', StrList, str], StrList]
