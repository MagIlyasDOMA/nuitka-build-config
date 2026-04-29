from typing import Literal, Optional, List, Callable, Self, Any, Tuple, Union, TypedDict, Dict
from subprocess import CompletedProcess
from pathlike_typing import PathLike

__all__ = ['BinFileType', 'PythonFlagType', 'NullStr', 'StrList', 'NonCliArguments',
           'NullPathLike', 'Verbosity', 'FilePathAndName', 'FileType', 'FilesList',
           'FieldType', 'TrueFalseDict', 'FieldTypeData', 'ArgvAddFunc', 'ProcessesList']

BinFileType = Literal['accelerated', 'onefile', 'standalone', 'module', 'app', 'app-dist', 'package', 'dll']
PythonFlagType = Literal['-S', 'no_site', '-O', 'no_asserts', 'no_warnings', 'no_docstrings', '-u', 'unbuffered']
NullStr = Optional[str]
StrList = List[str]
NullPathLike = Optional[PathLike]
Verbosity = Literal['quiet', 'info', 'verbose']

FilePathAndName = Tuple[PathLike, str]
FileType = Union[PathLike, FilePathAndName]
FilesList = List[FileType]

ArgvAddFunc = Callable[[Self, StrList, Any], StrList]

FieldType = Literal['str', 'int', 'bool', 'choice', 'ternary', 'strlist', 'filelist', 'custom', 'pathlike']


class TrueFalseDict(TypedDict):
    true: str
    false: str


FieldTypeData = Union[TrueFalseDict, Dict[str, str]]
ProcessesList = List[CompletedProcess]


class NonCliArguments(TypedDict):
    pre_compile_actions: StrList
    post_compile_actions: StrList
    time: bool

