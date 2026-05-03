from typing import TypedDict, Optional, Set, Literal
from pathlike_typing import PathLike
from ..typings import *

__all__ = ['IncludesDict', 'VersionInfoDict', 'WindowsParamsDict',
           'MacOSParamsDict', 'LinuxParamsDict', 'NuitkaConfigDict']

# ============ Includes ============
class IncludesDict(TypedDict, total=False):
    packages: StrList
    modules: StrList
    package_data: StrList
    files: FilesList
    directories: FilesList
    noinclude_data_files: StrList

# ============ VersionInfo ============
class VersionInfoDict(TypedDict, total=False):
    company_name: NullStr
    product_name: NullStr
    file_version: NullStr
    copyright_text: NullStr

# ============ BaseOSParams ============
class BaseOSParamsDict(TypedDict, total=False):
    icon: Optional[PathLike]

# ============ WindowsParams ============
class WindowsParamsDict(BaseOSParamsDict, total=False):
    console_mode: Literal['disable', 'force']
    uac_admin: bool
    uac_uiaccess: bool

# ============ MacOSParams ============
class MacOSParamsDict(BaseOSParamsDict, total=False):
    create_app_bundle: bool
    signed_app_name: NullStr

# ============ LinuxParams ============
class LinuxParamsDict(BaseOSParamsDict, total=False):
    pass

# ============ NuitkaConfig ============
class NuitkaConfigDict(TypedDict, total=False):
    type: BinFileType
    run: bool
    include: IncludesDict
    follow_imports: Optional[bool]
    follow_import_to: StrList
    nofollow_import_to: StrList
    plugins: StrList
    disable_plugins: StrList
    main: NullPathLike
    follow_stdlib: bool
    windows_params: WindowsParamsDict
    macos_params: MacOSParamsDict
    linux_params: LinuxParamsDict
    python_flags: Set[PythonFlagType]
    jobs: Optional[int]
    debug: bool
    report: NullPathLike
    output_dir: NullPathLike
    output_name: NullStr
    remove_output: bool
    extra_flags: StrList
    version_info: VersionInfoDict
    verbosity: Verbosity
    pre_compile_actions: StrList
    post_compile_actions: StrList
    time: bool
