import platform, sys, subprocess, shlex
from pathlib import Path
from typing import Optional, Set
from pathlike_typing import PathLike
from .decorators import argv_add
from .models import NuitkaConfig
from .typings import *
from .typings.models import *

__all__ = ['NuitkaBuilder']


class NuitkaBuilder:
    def __init__(self, config_path: PathLike = 'nbc-config.yaml', main: NullPathLike = None):
        self.config_path = Path(config_path)
        self.main = main

    def _parse_include_file(self, file: FileType) -> str:
        if isinstance(file, PathLike): return str(file)
        return '='.join(file)

    @argv_add
    def _add_type(self, argv: StrList, arg: str) -> StrList: return [f'--mode={arg}']

    @argv_add
    def _add_run(self, argv: StrList, arg: bool) -> StrList: return ['--run'] if arg else []

    @argv_add
    def _add_include(self, argv: StrList, arg: IncludesDict) -> StrList:
        output = list()
        output.extend([f'--include-package={package}' for package in arg['packages']])
        output.extend([f'--include-module={module}' for module in arg['modules']])
        output.extend([f'--include-package-data={package}'] for package in arg['package_data'])
        output.extend([f'--include-data-files={self._parse_include_file(file)}' for file in arg['files']])
        output.extend([f'--include-data-dir={self._parse_include_file(directory)}' for directory in arg['directories']])
        output.extend([f'--noinclude-data-files={pattern}' for pattern in arg['noinclude_data_files']])
        return output

    @argv_add
    def _add_follow_imports(self, argv: StrList, arg: Optional[bool]) -> StrList:
        if arg is None: return []
        elif arg: return ['--follow-imports']
        else: return ['--nofollow-imports']

    @argv_add
    def _add_follow_import_to(self, argv: StrList, arg: str) -> StrList:
        return [f'--follow-import-to={arg}']

    @argv_add
    def _add_nofollow_import_to(self, argv: StrList, arg: str) -> StrList:
        return [f'--nofollow-import-to={arg}']

    @argv_add
    def _add_plugins(self, argv: StrList, arg: StrList) -> StrList:
        return [f'--enable-plugins={plugin}' for plugin in arg]

    @argv_add
    def _add_disable_plugins(self, argv: StrList, arg: StrList) -> StrList:
        return [f'--disable-plugins={plugin}' for plugin in arg]

    @argv_add
    def _add_main(self, argv: StrList, arg: NullPathLike) -> StrList:
        main = arg or self.main
        return [f'--main={main}'] if main is None else []

    @argv_add
    def _add_follow_stdlib(self, argv: StrList, arg: bool) -> StrList:
        return ['--follow-stdlib'] if arg else []

    @argv_add
    def _add_windows_params(self, argv: StrList, arg: WindowsParamsDict) -> StrList:
        output = list()
        if platform.system() == 'Windows':
            icon = arg['icon']
            if icon:
                option = '--windows-icon-from-exe' if icon.endswith('.exe') \
                    else '--windows-icon-from-ico'
                output.append('='.join((option, str(icon))))
            output.append(f"--windows-console-mode={arg['console_mode']}")
            if arg['uac_admin']: output.append('--windows-uac-admin')
            if arg['uac_uiaccess']: output.append('--windows-uac-access')
        return output

    @argv_add
    def _add_macos_params(self, argv: StrList, arg: MacOSParamsDict) -> StrList:
        output = list()
        if platform.system() == 'Darwin':
            icon = arg['icon']
            if icon: output.append(f'--macos-app-icon={icon}')
            if arg['create_app_bundle']: output.append('--macos-create-app-bundle')
            signed_app_name = arg['signed_app_name']
            if signed_app_name: output.append(f'--macos-signed-app-name={signed_app_name}')
        return output

    @argv_add
    def _add_linux_params(self, argv: StrList, arg: LinuxParamsDict) -> StrList:
        output = list()
        if platform.system() == 'Linux':
            icon = arg['icon']
            if icon: output.append(f'--linux-icon={icon}')
        return output

    @argv_add
    def _add_python_flags(self, argv: StrList, arg: Set[PythonFlagType]) -> StrList:
        return [f'--python-flag={flag}' for flag in arg]

    @argv_add
    def _add_jobs(self, argv: StrList, arg: Optional[int]) -> StrList:
        return [f'--jobs={arg}'] if arg else []

    @argv_add
    def _add_debug(self, argv: StrList, arg: bool) -> StrList:
        return ['--debug'] if arg else []

    @argv_add
    def _add_report(self, argv: StrList, arg: NullPathLike) -> StrList:
        return ['--report'] if arg else []

    @argv_add
    def _add_output_dir(self, argv: StrList, arg: NullPathLike) -> StrList:
        return [f'--output-dir={arg}'] if arg else []

    @argv_add
    def _add_output_name(self, argv: StrList, arg: str) -> StrList:
        return [f'--output-name={arg}'] if arg else []

    @argv_add
    def _add_remove_output(self, argv: StrList, arg: bool) -> StrList:
        return ['--remove-output'] if arg else []

    @argv_add
    def _add_verbosity(self, argv: StrList, arg: Verbosity) -> StrList:
        match arg:
            case 'info': return []
            case 'quiet': return ['--quiet']
            case 'verbose': return ['--verbose']
            case _: raise KeyError(arg)

    @argv_add
    def _add_extra_flags(self, argv: StrList, arg: StrList) -> StrList: return arg

    @argv_add
    def _add_version_info(self, argv: StrList, arg: VersionInfoDict) -> StrList:
        output = list()
        for key in VersionInfoDict.__annotations__.keys():
            match key:
                case 'copyright_text': option_name = '--copyright'
                case _: option_name = f"--{key.replace('_', '-')}"
            value = arg[key] # type: ignore
            if value: output.append(f'{option_name}={value}')
        return output

    @staticmethod
    def _get_argv_add_method_name(attr_name: str):
        return f'_add_{attr_name}'

    @classmethod
    def _get_argv_add_method(cls, attr_name: str) -> ArgvAddMethod:
        return getattr(cls, cls._get_argv_add_method_name(attr_name))

    @property
    def config(self) -> NuitkaConfigDict:
        return NuitkaConfig.from_yaml_file(self.config_path).to_dict()

    @property
    def argv(self) -> StrList:
        argv = [sys.executable, '-m', 'nuitka']
        config: NuitkaConfigDict = self.config
        for key, value in config.items():
            self._get_argv_add_method(key)(self, argv, value)
        return argv

    @property
    def command(self) -> str:
        # TODO: Implement proper quoting of arguments
        argv = self.argv
        if platform.system() == 'Windows': return subprocess.list2cmdline(argv)
        return ' '.join(shlex.quote(arg) for arg in argv)

    def run(self, config_path: Optional[PathLike] = None) -> subprocess.CompletedProcess:
        if config_path is not None: self.config_path = config_path
        return subprocess.run(self.argv, text=True)
