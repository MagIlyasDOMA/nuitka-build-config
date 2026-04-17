import argparse
from pathlib import Path


class NuitkaParser(argparse.ArgumentParser):
    groups: dict

    def _add_config_root_arguments(self):
        self.add_argument('--mode', dest='type')
        self.add_argument('--run', dest='run')

        follow_imports_group = self.add_mutually_exclusive_group()
        self.groups['follow_imports'] = follow_imports_group
        follow_imports_group.add_argument('--follow-imports', action='store_const', const=True,
                                          dest='follow_imports')
        follow_imports_group.add_argument('--nofollow-imports', action='store_const', const=False,
                                          dest='follow_imports')

        self.add_argument('--follow-import-to', action='append', dest='follow_import_to')
        self.add_argument('--nofollow-import-to', action='append', dest='nofollow_import_to')
        self.add_argument('--enable-plugins', action='append', dest='plugins')
        self.add_argument('--disable-plugins', action='append', dest='disable_plugins')
        self.add_argument('--main', type=Path, dest='main')
        self.add_argument('--python-flag', action='append', dest='python_flags')
        self.add_argument('--jobs', type=int, dest='jobs')
        self.add_argument('--debug', action='store_true', dest='debug')
        self.add_argument('--report', type=Path, dest='report')
        self.add_argument('--output-dir', type=Path, dest='output_dir')
        self.add_argument('--output-name', dest='output_name')

        verbosity_group = self.add_mutually_exclusive_group()
        self.groups['verbosity'] = verbosity_group
        verbosity_group.add_argument('--verbose', action='store_const', const='verbose',
                                     dest='verbosity')
        verbosity_group.add_argument('--quiet', action='store_const', const='quiet',
                                     dest='verbosity')



    def _add_includes_arguments(self):
        includes_group = self.add_argument_group("Includes")
        self.groups['includes'] = includes_group
        includes_group.add_argument('--include-package', action='append',
                                    dest='includes__packages')
        includes_group.add_argument('--include-module', action='append',
                                    dest='includes__modules')
        includes_group.add_argument('--include-package-data', action='append',
                                    dest='includes__package_data')
        includes_group.add_argument('--include-data-files', action='append',
                                    dest='includes__files')
        includes_group.add_argument('--include-data-dir', action='append',
                                    dest='includes__directories')
        includes_group.add_argument('--noinclude-data-files', action='append',
                                    dest='includes__noinclude_data_files')

    def _add_windows_arguments(self):
        windows_group = self.add_argument_group("Windows parameters")
        self.groups['windows_params'] = windows_group
        windows__icon = windows_group.add_mutually_exclusive_group()
        self.groups['windows__icon'] = windows__icon
        windows__icon.add_argument('--windows-icon-from-ico',
                                   dest='windows__icon', type=Path)
        windows__icon.add_argument('--windows-icon-from-exe',
                                   dest='windows__icon', type=Path)
        windows_group.add_argument('--windows-console-mode', dest='windows__console_mode',
                                   choices=['disable', 'force'])
        windows_group.add_argument('--windows-uac-admin', action='store_true',
                                   dest='windows__uac_admin')
        windows_group.add_argument('--windows-uac-uiaccess', action='store_true',
                                   dest='windows__uac_uiaccess')

    def _add_macos_arguments(self):
        macos_group = self.add_argument_group("MacOS parameters")
        self.groups['macos_params'] = macos_group
        macos_group.add_argument('--macos-app-icon', dest='macos__icon', type=Path)
        macos_group.add_argument('--macos-create-app-bundle',
                          dest='macos__create_app_bundle', action='store_true')
        macos_group.add_argument('--macos-signed-app-name', dest='macos__signed_app_name')

    def _add_linux_arguments(self):
        linux_group = self.add_argument_group("Linux parameters")
        self.groups['linux_params'] = linux_group
        linux_group.add_argument('--linux-icon', dest='linux__icon', type=Path)

    def _add_version_info_arguments(self):
        version_info_group = self.add_argument_group("Version info")
        self.groups['version_info'] = version_info_group
        version_info_group.add_argument('--company-name', dest='version_info__company_name')
        version_info_group.add_argument('--product-name', dest='version_info__product_name')
        version_info_group.add_argument('--file-version', dest='version_info__file_version')
        version_info_group.add_argument('--copyright', dest='version_info__copyright_text')

