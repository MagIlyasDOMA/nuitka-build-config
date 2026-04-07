from typing import TypedDict, Optional, Literal
from pathlike_typing import PathLike

__all__ = ['BaseOSParams', 'WindowsParams', 'MacOSParams', 'LinuxParams']


class BaseOSParams(TypedDict, total=False):
    icon: Optional[PathLike]


class WindowsParams(BaseOSParams):
    console_mode: Literal['disable', 'force']
    uac_admin: bool


class MacOSParams(BaseOSParams):
    create_app_bundle: bool
    signed_app_name: str


class LinuxParams(BaseOSParams):
    pass
