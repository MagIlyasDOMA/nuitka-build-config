import sys
from argparse_help_i18n import HelpI18nMixin
from scparser import SubcommandsParser
from .builder import *
from .builder import main as builder_main
from .i18n import gettext
from .models import NuitkaConfig
from .generator import *
from .generator import main as generator_main
from .typings import NullStr
from .typings.models import NuitkaConfigDict

__all__ = ['NuitkaBuilder', 'NuitkaConfig', 'NuitkaConfigDict', 'main', '__version__',
           'NuitkaGenerator', 'GeneratorParser', 'GeneratorArgs', 'generator_main',
           'BuildRunOutput', 'BuilderParser', 'builder_main']
__version__ = '0.1.0'


class MainParser(SubcommandsParser, HelpI18nMixin): pass


def main():
    parser = MainParser()
    subparsers = parser.add_subparsers(dest='command')
    builder_parser =  subparsers.add_parser('build', parser=BuilderParser, help=gettext("Build a Nuitka project"))
    generator_parser = subparsers.add_parser('generate', parser=GeneratorParser, help=gettext("Generate a Nuitka config file"))
    help_parser = subparsers.add_parser('help', help=parser.get_help_message(), add_help=False)
    args = parser.parse_args()
    argv = sys.argv[2:] if len(sys.argv) > 2 else []
    match args.command:
        case 'build': NuitkaBuilder.cli_run(argv)
        case 'generate': NuitkaGenerator.cli_run(argv)
        case 'help':
            parser.print_help()
            sys.exit(0)
        case _: parser.error(f'Invalid command: {args.command}')


if __name__ == '__main__': main()
