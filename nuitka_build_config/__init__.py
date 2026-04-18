import argparse
from pathlib import Path
from .builder import NuitkaBuilder
from .models import NuitkaConfig
from .generator import NuitkaParser, GeneratorArgs, NuitkaGenerator, main as generator_main
from .typings.models import NuitkaConfigDict

__all__ = ['NuitkaBuilder', 'NuitkaConfig', 'NuitkaConfigDict', 'main', '__version__',
           'NuitkaGenerator', 'NuitkaParser', 'GeneratorArgs', 'generator_main']
__version__ = '0.1.0'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path', type=Path, help='Path to Nuitka config file',
                        nargs='?', default=None)
    parser.add_argument('main', type=Path, help='Path to main Nuitka build file',
                        nargs='?', default=None)
    parser.add_argument('--dry-run', action='store_true', help='Dry run')
    args = parser.parse_args()
    builder_ = NuitkaBuilder(args.config_path, args.main)
    if args.dry_run: print(builder_.argv)
    else: builder_.run()


if __name__ == '__main__': main()
