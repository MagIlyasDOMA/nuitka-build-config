import yaml
from typing import Optional, Set, cast
from pathlike_typing import PathLike
from pydantic import BaseModel, Field
from ..i18n import gettext
from ..typings import *
from ..typings.models import NuitkaConfigDict
from .osparams import *


class Includes(BaseModel):
    packages: StrList = Field(default_factory=list,
                              description=gettext("List of packages to include in the build (--include-package)"))
    modules: StrList = Field(default_factory=list,
                             description=gettext("List of modules to include in the build (--include-module)"))
    package_data: StrList = Field(default_factory=list,
                                  description=gettext("Packages whose data files should be included (--include-package-data)"))
    files: FilesList = Field(default_factory=list, description=gettext("File patterns to include (--include-data-files)"))
    directories: FilesList = Field(default_factory=list,
                                 description=gettext("Data directories to include (--include-data-dir)"))
    noinclude_data_files: StrList = Field(default_factory=list,
                                          description=gettext("File patterns to exclude from data (--noinclude-data-files)"))


class VersionInfo(BaseModel):
    company_name: NullStr = Field(default=None, description=gettext("Company name in version info (--company-name)"))
    product_name: NullStr = Field(default=None, description=gettext("Product name in version info (--product-name)"))
    file_version: NullStr = Field(default=None, description=gettext("File version in X.X.X.X format (--file-version)"))
    copyright_text: NullStr = Field(default=None, description=gettext("Copyright text (--copyright)"))


class NuitkaConfig(BaseModel):
    type: BinFileType = Field(
        default='accelerated',
        description=gettext("Compilation mode: 'accelerated' (with Python dependency), 'standalone' (folder with exe), "
                    "'onefile' (single exe), 'module' (extension module), 'app' (onefile for macOS with .app), "
                    "'app-dist' (standalone for macOS with .app), 'package' (package as module), 'dll' (experimental)")
    )

    run: bool = Field(
        default=False,
        description=gettext("Run the compiled binary immediately after compilation (--run)")
    )

    include: Includes = Field(
        default_factory=Includes,
        description=gettext("Settings for including additional modules, packages and data files")
    )

    follow_imports: Optional[bool] = Field(
        default=None,
        description=gettext("Follow all imported modules. In standalone mode defaults to True (--follow-imports)")
    )

    follow_import_to: StrList = Field(
        default_factory=list,
        description=gettext("Follow into the specified modules/packages (--follow-import-to). Example: 'requests', 'numpy'")
    )

    nofollow_import_to: StrList = Field(
        default_factory=list,
        description=gettext("DO NOT follow into the specified modules/packages. Supports patterns, e.g. '*.tests' (--nofollow-import-to)")
    )

    plugins: StrList = Field(
        default_factory=list,
        description=gettext("List of plugins to enable (--enable-plugins). Example: 'tk-inter', 'anti-bloat'")
    )

    disable_plugins: StrList = Field(
        default_factory=list,
        description=gettext("List of plugins to disable (--disable-plugins)")
    )

    main: NullPathLike = Field(
        default=None,
        description=gettext("Main file to compile (alternative to positional argument --main)")
    )

    follow_stdlib: bool = Field(
        default=False,
        description=gettext("Follow into standard library modules. Increases compilation time (--follow-stdlib)")
    )

    windows_params: WindowsParams = Field(
        default_factory=WindowsParams,
        description=gettext("Windows parameters: console mode, UAC, icon, etc.")
    )

    macos_params: MacOSParams = Field(
        default_factory=MacOSParams,
        description=gettext("macOS parameters: .app bundle creation, signing, version, etc.")
    )

    linux_params: LinuxParams = Field(
        default_factory=LinuxParams,
        description=gettext("Linux parameters: icon and other settings")
    )

    python_flags: Set[PythonFlagType] = Field(
        default_factory=set,
        description=gettext("Python flags: '-S' (no_site), '-O' (no_asserts), 'no_warnings', 'no_docstrings', '-u' (unbuffered)")
    )

    jobs: Optional[int] = Field(
        default=None,
        description=gettext("Number of parallel compilation jobs. Negative values = CPU cores minus value (--jobs)")
    )

    debug: bool = Field(
        default=False,
        description=gettext("Enable debug mode: self-checks, additional checks (--debug)")
    )

    report: NullPathLike = Field(
        default=None,
        description=gettext("Create an XML compilation report (--report)")
    )

    output_dir: NullPathLike = Field(
        default=None,
        description=gettext("Directory for output files (build, dist, binaries) (--output-dir)")
    )

    output_name: NullStr = Field(
        default=None,
        description=gettext("Name of the output executable. For onefile may include path (--output-filename)")
    )

    remove_output: bool = Field(
        default=False,
        description=gettext("Remove the build directory after creating the binary (--remove-output)")
    )

    extra_flags: StrList = Field(
        default_factory=list,
        description=gettext("Additional Nuitka command line flags not described in this model")
    )

    version_info: VersionInfo = Field(
        default_factory=VersionInfo,
        description=gettext("Version info for Windows/macOS: company name, product name, file version, copyright")
    )

    verbosity: Verbosity = Field(
        default='info',
        description=gettext("Console output verbosity level: info (default), quiet, verbose")
    )

    pre_compile_actions: StrList = Field(
        default_factory=list,
        description=gettext("Commands executed before compilation")
    )

    post_compile_actions: StrList = Field(
        default_factory=list,
        description=gettext("Commands executed after compilation")
    )

    model_config = dict(
        title='nuitka-build-config',
        description='nuitka build config',
    )

    @classmethod
    def from_yaml_file(cls, path: PathLike) -> NuitkaConfig:
        with open(path, encoding='utf-8') as file:
            data = yaml.safe_load(file)
            if not isinstance(data, dict): data = dict()
        return cls.model_validate(data)

    def to_dict(self) -> NuitkaConfigDict:
        return model2dict(self) # type: ignore


def model2dict(model: BaseModel) -> dict:
    output = dict(model)
    for key, value in output.copy().items():
        if isinstance(value, BaseModel): output[key] = model2dict(value)
    return output
