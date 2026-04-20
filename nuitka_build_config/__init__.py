import argparse
from pathlib import Path
from .builder import *
from .models import NuitkaConfig
from .generator import NuitkaParser, GeneratorArgs, NuitkaGenerator, main as generator_main
from .typings.models import NuitkaConfigDict

__all__ = ['NuitkaBuilder', 'NuitkaConfig', 'NuitkaConfigDict', 'main', '__version__',
           'NuitkaGenerator', 'NuitkaParser', 'GeneratorArgs', 'generator_main',
           'BuildRunOutput', 'BuilderParser']
__version__ = '0.1.0'


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.add_parser()
    args = parser.parse_args()
    builder_ = NuitkaBuilder(args.config_path, args.main)
    if args.dry_run: print(builder_.argv)
    else: builder_.run()


if __name__ == '__main__': main()
