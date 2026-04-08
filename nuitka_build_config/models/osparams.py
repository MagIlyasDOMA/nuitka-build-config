from typing import Optional, Literal
from pathlike_typing import PathLike
from pydantic import BaseModel, Field
from ..i18n import gettext
from ..typings import NullStr

__all__ = ['BaseOSParams', 'WindowsParams', 'MacOSParams', 'LinuxParams']


class BaseOSParams(BaseModel):
    icon: Optional[PathLike] = Field(
        default=None,
        description=gettext("Path to icon file. On Windows: --windows-icon-from-ico, on macOS: --macos-app-icon, on Linux: --linux-icon")
    )


class WindowsParams(BaseOSParams):
    console_mode: Literal['disable', 'force'] = Field(
        default='force',
        description=gettext("Windows console mode: 'force' - create a console window (if not started from console), "
                    "'disable' - do not create a console (--windows-console-mode)")
    )

    uac_admin: bool = Field(
        default=False,
        description=gettext("Request administrator privileges via UAC on launch (--windows-uac-admin)")
    )

    uac_uiaccess: bool = Field(
        default=False,
        description=gettext("Request UAC to launch only from specific folders and remote access (--windows-uac-uiaccess)")
    )


class MacOSParams(BaseOSParams):
    create_app_bundle: bool = Field(
        default=False,
        description=gettext("Create a .app bundle instead of a regular binary. Enables standalone mode (--macos-create-app-bundle)")
    )

    signed_app_name: NullStr = Field(
        default=None,
        description=gettext("Application name for macOS signing in 'com.YourCompany.AppName' format. "
                    "Globally unique identifier for accessing protected APIs (--macos-signed-app-name)")
    )


class LinuxParams(BaseOSParams):
    pass