import platform, sys, subprocess, shlex
from typing import Optional
from pathlib import Path
from pathlike_typing import PathLike
from .base import DecoratorMixin, BaseParser
from .decorators import dataclass
from .i18n import gettext
from .models import NuitkaConfig
from .typings import *
from .typings.models import NuitkaConfigDict

__all__ = ['NuitkaBuilder', 'BuildRunOutput', 'BuilderParser', 'main']


class BuilderParser(BaseParser):
    def add_arguments(self):
        self.add_argument('config_path', type=Path, help=gettext('Path to Nuitka config file'),
                            nargs='?', default=None)
        self.add_argument('main', type=Path, help=gettext('Path to main Nuitka build file'),
                            nargs='?', default=None)
        self.add_argument('--dry-run', action='store_true', help=gettext('Dry run'))


@dataclass
class BuildRunOutput:
    pre: ProcessesList
    main: subprocess.CompletedProcess
    post: ProcessesList


class NuitkaBuilder(DecoratorMixin):
    @staticmethod
    def _field_is_cli(field_name: str) -> bool:
        field = NuitkaConfig.model_fields[field_name]
        return not getattr(field, 'json_schema_extra', dict()).get('non_cli', False)

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
            if self._field_is_cli(key): self._get_argv_add_method(key)(self, argv, value)
        return argv

    @property
    def non_cli_arguments(self) -> NonCliArguments:
        output = dict()
        for key, value in self.config.items():
            if not self._field_is_cli(key): output[key] = value
        return output # type: ignore

    @property
    def command(self) -> str:
        # TODO: Implement proper quoting of arguments
        argv = self.argv
        if platform.system() == 'Windows': return subprocess.list2cmdline(argv)
        return ' '.join(shlex.quote(arg) for arg in argv)

    def run(self, config_path: Optional[PathLike] = None) -> BuildRunOutput:
        if config_path is not None: self.config_path = config_path
        non_cli_arguments: NonCliArguments = self.non_cli_arguments
        pre_processes = list()
        post_processes = list()
        for command in non_cli_arguments['pre_compile_actions']:
            pre_processes.append(subprocess.run(command, text=True, shell=True))
        for command in non_cli_arguments['post_compile_actions']:
            post_processes.append(subprocess.run(command, text=True, shell=True))
        main_ = subprocess.run(self.argv, text=True)
        return BuildRunOutput(pre=pre_processes, main=main_, post=post_processes)

    @classmethod
    def cli_run(cls) -> Optional[BuildRunOutput]:
        parser = BuilderParser()
        args = parser.parse_args()
        builder = cls(args.config_path, args.main)
        if args.dry_run:
            return None
        return builder.run()


def main(): NuitkaBuilder.cli_run()


if __name__ == '__main__': main()

