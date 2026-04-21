import yaml
from typing import Self, Tuple, Dict
from pathlib import Path
from pathlike_typing import PathLike
from .base import BaseParser
from .decorators import dataclass
from .builder import NuitkaBuilder
from .i18n import gettext
from .models import NuitkaConfig
from .typings import NullStr
from .typings.models import NuitkaConfigDict

__all__ = ['GeneratorParser', 'GeneratorArgs', 'NuitkaGenerator', 'main']


@dataclass
class GeneratorArgs:
    output_file: str
    compile: bool


class GeneratorParser(BaseParser):
    def __init__(self, *args, epilog: NullStr = None, **kwargs):
        if epilog is None: epilog = gettext("Extra arguments are added to extra_flags")
        super().__init__(*args, **kwargs, epilog=epilog)

    def _add_config_root_arguments(self):
        self.add_argument('--mode', dest='type',
                          help=gettext("Compilation mode: 'accelerated' (with Python dependency), 'standalone' (folder with exe), "
                                       "'onefile' (single exe), 'module' (extension module), 'app' (onefile for macOS with .app), "
                                       "'app-dist' (standalone for macOS with .app), 'package' (package as module), 'dll' (experimental)"))
        self.add_argument('--run', dest='run', action='store_true',
                          help=gettext("Run the compiled binary immediately after compilation (--run)"))

        follow_imports_group = self.add_mutually_exclusive_group()
        follow_imports_group.add_argument('--follow-imports', action='store_const', const=True, dest='follow_imports',
                                          help=gettext("Follow all imported modules. In standalone mode defaults to True"))
        follow_imports_group.add_argument('--nofollow-imports', action='store_const', const=False, dest='follow_imports',
                                          help=gettext("DO NOT follow all imported modules"))

        self.add_argument('--follow-import-to', action='append', dest='follow_import_to',
                          help=gettext("Follow into the specified modules/packages. Example: 'requests', 'numpy'"))
        self.add_argument('--nofollow-import-to', action='append', dest='nofollow_import_to',
                          help=gettext("DO NOT follow into the specified modules/packages. Supports patterns, e.g. '*.tests'"))
        self.add_argument('--enable-plugins', action='append', dest='plugins',
                          help=gettext("List of plugins to enable. Example: 'tk-inter', 'anti-bloat'"))
        self.add_argument('--disable-plugins', action='append', dest='disable_plugins',
                          help=gettext("List of plugins to disable"))
        self.add_argument('--main', type=Path, dest='main',
                          help=gettext("Main file to compile (alternative to positional argument --main)"))
        self.add_argument('main_pos', type=Path, metavar='MAIN', nargs='?',
                          help=gettext("Main file to compile (positional argument)"))
        self.add_argument('--python-flag', action='append', dest='python_flags',
                          help=gettext("Python flags: '-S' (no_site), '-O' (no_asserts), 'no_warnings', 'no_docstrings', '-u' (unbuffered)"))
        self.add_argument('--jobs', type=int, dest='jobs',
                          help=gettext("Number of parallel compilation jobs. Negative values = CPU cores minus value (--jobs)"))
        self.add_argument('--debug', action='store_true', dest='debug',
                          help=gettext("Enable debug mode: self-checks, additional checks (--debug)"))
        self.add_argument('--report', type=Path, dest='report',
                          help=gettext("Create an XML compilation report (--report)"))
        self.add_argument('--output-dir', type=Path, dest='output_dir',
                          help=gettext("Directory for output files (build, dist, binaries) (--output-dir)"))
        self.add_argument('--output-name', dest='output_name',
                          help=gettext("Name of the output executable. For onefile may include path (--output-filename)"))
        self.add_argument('--remove-output', action='store_true', dest='remove_output',
                          help=gettext("Remove the build directory after creating the binary (--remove-output)"))

        verbosity_group = self.add_mutually_exclusive_group()
        verbosity_group.add_argument('--verbose', action='store_const', const='verbose', dest='verbosity',
                                     help=gettext("Console output verbosity level: verbose"))
        verbosity_group.add_argument('--quiet', action='store_const', const='quiet', dest='verbosity',
                                     help=gettext("Console output verbosity level: quiet"))
        self.set_defaults(verbosity='info', type='accelerated')

    def _add_includes_arguments(self):
        includes_group = self.add_argument_group("Includes",
                                                 description=gettext("Settings for including additional modules, packages and data files"))
        includes_group.add_argument('--include-package', action='append', dest='include__packages',
                                    metavar='PACKAGES', help=gettext("List of packages to include in the build (--include-package)"))
        includes_group.add_argument('--include-module', action='append', dest='include__modules',
                                    metavar='MODULES', help=gettext("List of modules to include in the build (--include-module)"))
        includes_group.add_argument('--include-package-data', action='append', dest='include__package_data',
                                    metavar='PACKAGE_DATA',
                                    help=gettext("Packages whose data files should be included (--include-package-data)"))
        includes_group.add_argument('--include-data-files', action='append', dest='include__files',
                                    metavar='FILES', help=gettext("File patterns to include (--include-data-files)"))
        includes_group.add_argument('--include-data-dir', action='append', dest='include__directories',
                                    metavar='DIRECTORIES', help=gettext("Data directories to include (--include-data-dir)"))
        includes_group.add_argument('--noinclude-data-files', action='append', dest='include__noinclude_data_files',
                                    metavar='NOINCLUDE_DATA_FILES', help=gettext("File patterns to exclude from data (--noinclude-data-files)"))

    def _add_windows_arguments(self):
        windows_group = self.add_argument_group("Windows parameters")
        windows_params__icon = windows_group.add_mutually_exclusive_group()
        windows_params__icon.add_argument('--windows-icon-from-ico', dest='windows_params__icon', type=Path,
                                          metavar='ICON', help=gettext("Path to icon file (ICO format)"))
        windows_params__icon.add_argument('--windows-icon-from-exe', dest='windows_params__icon', type=Path,
                                          metavar='ICON', help=gettext("Extract icon from existing EXE file"))
        windows_group.add_argument('--windows-console-mode', dest='windows_params__console_mode',
                                   choices=['disable', 'force'], metavar='CONSOLE_MODE',
                                   help=gettext("Windows console mode: 'force' - create a console window (if not started from console), "
                                                "'disable' - do not create a console (--windows-console-mode)"))
        windows_group.add_argument('--windows-uac-admin', action='store_true', dest='windows_params__uac_admin',
                                   help=gettext("Request administrator privileges via UAC on launch (--windows-uac-admin)"))
        windows_group.add_argument('--windows-uac-uiaccess', action='store_true', dest='windows_params__uac_uiaccess',
                                   help=gettext("Request UAC to launch only from specific folders and remote access (--windows-uac-uiaccess)"))

    def _add_macos_arguments(self):
        macos_group = self.add_argument_group("MacOS parameters")
        macos_group.add_argument('--macos-app-icon', dest='macos_params__icon', type=Path,
                                 metavar='ICON',
                                 help=gettext("Path to icon file for macOS .app bundle (--macos-app-icon)"))
        macos_group.add_argument('--macos-create-app-bundle', dest='macos_params__create_app_bundle', action='store_true',
                                 help=gettext("Create a .app bundle instead of a regular binary. Enables standalone mode (--macos-create-app-bundle)"))
        macos_group.add_argument('--macos-signed-app-name', dest='macos_params__signed_app_name',
                                 metavar='SIGNED_APP_NAME',
                                 help=gettext("Application name for macOS signing in 'com.YourCompany.AppName' format. "
                                              "Globally unique identifier for accessing protected APIs (--macos-signed-app-name)"))

    def _add_linux_arguments(self):
        linux_group = self.add_argument_group("Linux parameters")
        linux_group.add_argument('--linux-icon', dest='linux_params__icon', type=Path,
                                 metavar='ICON',
                                 help=gettext("Path to icon file for Linux (--linux-icon)"))

    def _add_version_info_arguments(self):
        version_info_group = self.add_argument_group("Version info")
        version_info_group.add_argument('--company-name', dest='version_info__company_name',
                                        metavar='COMPANY_NAME',
                                        help=gettext("Company name in version info (--company-name)"))
        version_info_group.add_argument('--product-name', dest='version_info__product_name',
                                        metavar='PRODUCT_NAME',
                                        help=gettext("Product name in version info (--product-name)"))
        version_info_group.add_argument('--file-version', dest='version_info__file_version',
                                        metavar='FILE_VERSION',
                                        help=gettext("File version in X.X.X.X format (--file-version)"))
        version_info_group.add_argument('--copyright', dest='version_info__copyright_text',
                                        metavar='COPYRIGHT_TEXT',
                                        help=gettext("Copyright text (--copyright)"))

    def _add_actions_arguments(self):
        actions_group = self.add_argument_group(gettext("Actions"), gettext("Add commands to run before or after compilation"))
        actions_group.add_argument('--add-pre-compile-action', '-b',
                                   dest='pre_compile_actions', help=gettext("Commands executed before compilation"))
        actions_group.add_argument('--add-post-compile-action', '-p',
                                   dest='post_compile_actions', help=gettext("Commands executed after compilation"))

    def _add_non_config_arguments(self):
        non_config_group = self.add_argument_group(gettext("Non-config arguments"),
                                                   gettext("Arguments that are not written to the configuration file"))
        non_config_group.add_argument('--output-file', '-o', default='nbc-config.yaml',
                                      dest='non_config__output_file', metavar='FILE', help=gettext("Path to output file"))
        non_config_group.add_argument('--compile', '-c', action='store_true',
                                      dest='non_config__compile', help=gettext("Compile the application after generating the configuration file"))

    def add_arguments(self) -> Self:
        self.add_argument('--version', '-v', action='version', help=gettext("show program's version number and exit"))
        self._add_config_root_arguments()
        self._add_includes_arguments()
        self._add_windows_arguments()
        self._add_macos_arguments()
        self._add_linux_arguments()
        self._add_version_info_arguments()
        self._add_actions_arguments()
        self._add_non_config_arguments()
        return self

    def _validate_main(self, dct: dict, /) -> str:
        main_opt = dct.get('main', None)
        main_pos = dct.pop('main_pos') if 'main_pos' in dct else None
        if not main_pos and not main_opt: self.error(gettext("'main' option is required"))
        elif main_pos and main_opt: self.error(gettext("Use either just --main or just the positional argument"))
        output = main_pos or main_opt
        dct['main'] = output
        return output

    def parse_to_dicts(self, args=None, add_nones: bool = False) -> Tuple[NuitkaConfigDict, Dict[str, str]]:
        args, extra = self.parse_known_args(args)
        raw_dict = vars(args)
        self._validate_main(raw_dict)
        raw_dict['extra_flags'] = extra
        output = dict()
        non_config_items = dict()
        for key, value in raw_dict.items():
            if value is None and not add_nones: continue
            if '__' not in key: output[key] = value
            else:
                namespace, key = key.split('__', 1)
                if namespace == 'non_config': non_config_items[key] = value
                if namespace not in output: output[namespace] = dict()
                output[namespace][key] = value
        return output, non_config_items # type: ignore

    def parse_to_objects(self, args=None, add_nones: bool = False) -> Tuple[NuitkaConfig, GeneratorArgs]:
        config, non_config_items = self.parse_to_dicts(args, add_nones)
        return NuitkaConfig.model_validate(config), GeneratorArgs(**non_config_items)


class NuitkaGenerator:
    @staticmethod
    def generate_file(config: NuitkaConfig, path: PathLike, compile: bool):
        with open(path, 'w', encoding='utf-8') as file:
            file.write("# $schema: https://raw.githubusercontent.com/MagIlyasDOMA/nuitka-build-config/refs/heads/main/schema.json\n\n")
            yaml.safe_dump(config.to_dict(), file, allow_unicode=True)
        if compile: NuitkaBuilder().run(path)

    @classmethod
    def cli_run(cls):
        parser = GeneratorParser()
        config, non_config = parser.parse_to_objects()
        cls.generate_file(config, non_config.output_file, non_config.compile)


def main(): NuitkaGenerator.cli_run()

if __name__ == '__main__': main()
