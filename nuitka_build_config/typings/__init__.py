from typing import Literal, Optional, List, Callable, Self, Any
from pathlike_typing import PathLike

__all__ = ['BinFileType', 'PythonFlagType', 'NullStr', 'StrList', 'ArgvAddMethod', 'NullPathLike', 'Verbosity']

BinFileType = Literal['accelerated', 'onefile', 'standalone', 'module', 'app', 'app-dist', 'package', 'dll']
PythonFlagType = Literal['-S', 'no_site', '-O', 'no_asserts', 'no_warnings', 'no_docstrings', '-u', 'unbuffered']
NullStr = Optional[str]
StrList = List[str]
NullPathLike = Optional[PathLike]
Verbosity = Literal['quiet', 'info', 'verbose']

ArgvAddMethod = Callable[[Self, StrList, Any], StrList]
