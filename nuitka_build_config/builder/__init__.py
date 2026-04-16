import platform, sys, subprocess, shlex
from pathlib import Path
from typing import Optional
from pathlike_typing import PathLike
from .. import NuitkaConfig
from ..typings import *
from ..typings.models import NuitkaConfigDict
from .base import DecoratorMixin

__all__ = ['NuitkaBuilder']


class NuitkaBuilder(DecoratorMixin):
    @staticmethod
    def _get_argv_add_method_name(attr_name: str):
        return f'_add_{attr_name}'

    @classmethod
    def _get_argv_add_method(cls, attr_name: str) -> ArgvAddFunc:
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
