from typing import Literal, List, Optional, TypedDict
from pathlike_typing import PathLike
from pydantic import BaseModel
from .osparams import *

BinFileType = Literal['accelerated', 'onefile', 'standalone', 'module']


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
    python_flags: List = []
    enable_lto: bool = False
    jobs: int
    debug: bool = False
    report: bool = False
