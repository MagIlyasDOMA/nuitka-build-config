from typing import Literal, List, Optional, TypedDict, Set
from pathlike_typing import PathLike
from pydantic import BaseModel
from .osparams import *

BinFileType = Literal['accelerated', 'onefile', 'standalone', 'module', 'app', 'app-dist', 'package', 'dll']
PythonFlagType = Literal['-S', 'no_site', '-O', 'no_asserts', 'no_warnings', 'no_docstrings', '-u', 'undefined']


class Includes(TypedDict, total=False):
    packages: List[str]
    modules: List[str]
    package_data: List[str]
    files: List[str]
    directories: List[str]
    noinclude_data_files: List[str]


class NuitkaConfig(BaseModel):
    type: BinFileType = 'accelerated'
    run: bool = False
    include: Includes = {}
    follow_imports: Optional[bool] = None
    follow_import_to: List[str] = []
    nofollow_import_to: List[str] = []
    plugins: List[str] = []
    disable_plugins: List[str] = []
    main: Optional[PathLike] = None
    follow_stdlib: bool = False
    windows_params: WindowsParams = {}
    macos_params: MacOSParams = {}
    linux_params: LinuxParams = {}
    python_flags: Set[PythonFlagType] = []
    jobs: Optional[int] = None
    debug: bool = False
    report: bool = False
    output_dir: Optional[PathLike] = None
    output_filename: Optional[str] = None
    remove_output: bool = False
