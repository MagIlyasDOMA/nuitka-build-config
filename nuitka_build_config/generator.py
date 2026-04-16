import argparse
from pathlib import Path


class NuitkaParser(argparse.ArgumentParser):
    groups: dict

    def _add_config_root_arguments(self):
        self.add_argument('--mode', dest='type')
        self.add_argument('--run')

        follow_imports_group = self.add_mutually_exclusive_group()
        self.groups['follow_imports'] = follow_imports_group
        follow_imports_group.add_argument('--follow-imports', action='store_const', const=True,
                                          dest='follow_imports')
        follow_imports_group.add_argument('--nofollow-imports', action='store_const', const=False,
                                          dest='follow_imports')

        self.add_argument('--follow-import-to', action='append')
        self.add_argument('--nofollow-import-to', action='append')
        self.add_argument('--enable-plugins', action='append', dest='plugins')
        self.add_argument('--disable-plugins', action='append')
        self.add_argument('--main', type=Path)
        self.add_argument('--python-flag', action='append', dest='python_flags')
        self.add_argument('--jobs', type=int)
        self.add_argument('--debug', action='store_true')
        self.add_argument('--report', type=Path)
        self.add_argument('--output-dir', type=Path)
        self.add_argument('--output-name')

        verbosity_group = self.add_mutually_exclusive_group()
        self.groups['verbosity'] = verbosity_group
        verbosity_group.add_argument('--verbose', action='store_const', const='verbose',
                                     dest='verbosity')
        verbosity_group.add_argument('--quiet', action='store_const', const='quiet',
                                     dest='verbosity')

    def _add_includes_arguments(self):
        raise NotImplementedError

    def _add_windows_arguments(self):
        raise NotImplementedError

    def _add_macos_arguments(self):
        raise NotImplementedError

    def _add_linux_arguments(self):
        raise NotImplementedError

    def _add_version_info_arguments(self):
        raise NotImplementedError

