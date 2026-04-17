import argparse
from pathlib import Path
from .i18n import gettext
from .models import NuitkaConfig
from .typings.models import NuitkaConfigDict


class GroupsDictMixin(argparse.ArgumentParser):
    groups: dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = dict()

    def add_argument_group(
            self,
            title=None,
            description=None,
            name: str = ...,
            *,
            prefix_chars=...,
            argument_default=...,
            conflict_handler=...,
    ) -> argparse._ArgumentGroup:
        group = super().add_argument_group(
            title, description, prefix_chars=prefix_chars,
            argument_default=argument_default, conflict_handler=conflict_handler
        )
        self.groups[name] = group
        return group

    def add_mutually_exclusive_group(self, *, required=False, name: str = ...) -> argparse._MutuallyExclusiveGroup:
        group = super().add_mutually_exclusive_group(required=required)
        self.groups[name] = group
        return group


class NuitkaParser(GroupsDictMixin):
    def _add_config_root_arguments(self):
        self.add_argument('--mode', dest='type',
                          help=gettext("Compilation mode: 'accelerated' (with Python dependency), 'standalone' (folder with exe), "
                                       "'onefile' (single exe), 'module' (extension module), 'app' (onefile for macOS with .app), "
                                       "'app-dist' (standalone for macOS with .app), 'package' (package as module), 'dll' (experimental)"))
        self.add_argument('--run', dest='run', action='store_true',
                          help=gettext("Run the compiled binary immediately after compilation (--run)"))

        follow_imports_group = self.add_mutually_exclusive_group(name='follow_imports')
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
        self.add_argument('main', type=Path, dest='main', nargs='?',
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
        includes_group = self.add_argument_group("Includes", name='include',
            description=gettext("Settings for including additional modules, packages and data files"))
        includes_group.add_argument('--include-package', action='append', dest='includes__packages',
                                    help=gettext("List of packages to include in the build (--include-package)"))
        includes_group.add_argument('--include-module', action='append', dest='includes__modules',
                                    help=gettext("List of modules to include in the build (--include-module)"))
        includes_group.add_argument('--include-package-data', action='append', dest='includes__package_data',
                                    help=gettext("Packages whose data files should be included (--include-package-data)"))
        includes_group.add_argument('--include-data-files', action='append', dest='includes__files',
                                    help=gettext("File patterns to include (--include-data-files)"))
        includes_group.add_argument('--include-data-dir', action='append', dest='includes__directories',
                                    help=gettext("Data directories to include (--include-data-dir)"))
        includes_group.add_argument('--noinclude-data-files', action='append', dest='includes__noinclude_data_files',
                                    help=gettext("File patterns to exclude from data (--noinclude-data-files)"))

    def _add_windows_arguments(self):
        windows_group = self.add_argument_group("Windows parameters", name='windows_params')
        windows__icon = windows_group.add_mutually_exclusive_group()
        windows__icon.add_argument('--windows-icon-from-ico', dest='windows__icon', type=Path,
                                   help=gettext("Path to icon file (ICO format)"))
        windows__icon.add_argument('--windows-icon-from-exe', dest='windows__icon', type=Path,
                                   help=gettext("Extract icon from existing EXE file"))
        windows_group.add_argument('--windows-console-mode', dest='windows__console_mode',
                                   choices=['disable', 'force'],
                                   help=gettext("Windows console mode: 'force' - create a console window (if not started from console), "
                                                "'disable' - do not create a console (--windows-console-mode)"))
        windows_group.add_argument('--windows-uac-admin', action='store_true', dest='windows__uac_admin',
                                   help=gettext("Request administrator privileges via UAC on launch (--windows-uac-admin)"))
        windows_group.add_argument('--windows-uac-uiaccess', action='store_true', dest='windows__uac_uiaccess',
                                   help=gettext("Request UAC to launch only from specific folders and remote access (--windows-uac-uiaccess)"))

    def _add_macos_arguments(self):
        macos_group = self.add_argument_group("MacOS parameters", name='macos_params')
        macos_group.add_argument('--macos-app-icon', dest='macos__icon', type=Path,
                                 help=gettext("Path to icon file for macOS .app bundle (--macos-app-icon)"))
        macos_group.add_argument('--macos-create-app-bundle', dest='macos__create_app_bundle', action='store_true',
                                 help=gettext("Create a .app bundle instead of a regular binary. Enables standalone mode (--macos-create-app-bundle)"))
        macos_group.add_argument('--macos-signed-app-name', dest='macos__signed_app_name',
                                 help=gettext("Application name for macOS signing in 'com.YourCompany.AppName' format. "
                                              "Globally unique identifier for accessing protected APIs (--macos-signed-app-name)"))

    def _add_linux_arguments(self):
        linux_group = self.add_argument_group("Linux parameters", name='linux_params')
        linux_group.add_argument('--linux-icon', dest='linux__icon', type=Path,
                                 help=gettext("Path to icon file for Linux (--linux-icon)"))

    def _add_version_info_arguments(self):
        version_info_group = self.add_argument_group("Version info", name='version_info')
        version_info_group.add_argument('--company-name', dest='version_info__company_name',
                                        help=gettext("Company name in version info (--company-name)"))
        version_info_group.add_argument('--product-name', dest='version_info__product_name',
                                        help=gettext("Product name in version info (--product-name)"))
        version_info_group.add_argument('--file-version', dest='version_info__file_version',
                                        help=gettext("File version in X.X.X.X format (--file-version)"))
        version_info_group.add_argument('--copyright', dest='version_info__copyright_text',
                                        help=gettext("Copyright text (--copyright)"))

    def _add_actions_arguments(self):
        actions_group = self.add_argument_group("Actions", name='actions')
        actions_group.add_argument('--add-pre-compile-action', '-b',
                                   dest='pre_compile_actions', help=gettext("Commands executed before compilation"))
        actions_group.add_argument('--add-post-compile-action', '-p',
                                   dest='post_compile_actions', help=gettext("Commands executed after compilation"))

    def add_arguments(self):
        self._add_config_root_arguments()
        self._add_includes_arguments()
        self._add_windows_arguments()
        self._add_macos_arguments()
        self._add_linux_arguments()
        self._add_version_info_arguments()
        self._add_actions_arguments()

    def parse_to_dict(self, args=None, add_nones: bool = False) -> NuitkaConfigDict:
        args, extra = self.parse_known_args(args)
        raw_dict = vars(args)
        raw_dict['extra_flags'] = extra
        output = dict()
        for key, value in raw_dict.items():
            if value is None and not add_nones: continue
            if '__' in key: output[key] = value
            else:
                namespace, key = key.split('__', 1)
                if namespace not in output: output[namespace] = dict()
                output[namespace][key] = value
        return output # type: ignore

    def parse_to_object(self, args=None, add_nones: bool = False) -> NuitkaConfig:
        return NuitkaConfig.model_validate(self.parse_to_dict(args, add_nones))


def main():
    parser = NuitkaParser()
    args = parser.parse_to_object()


if __name__ == '__main__':
    main()
