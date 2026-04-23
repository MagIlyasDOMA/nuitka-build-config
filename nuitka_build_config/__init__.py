import argparse
from .builder import *
from .builder import main as builder_main
from .models import NuitkaConfig
from .generator import *
from .generator import main as generator_main
from .typings.models import NuitkaConfigDict

__all__ = ['NuitkaBuilder', 'NuitkaConfig', 'NuitkaConfigDict', 'main', '__version__',
           'NuitkaGenerator', 'GeneratorParser', 'GeneratorArgs', 'generator_main',
           'BuildRunOutput', 'BuilderParser', 'builder_main']
__version__ = '0.1.0'


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    builder_parser =  subparsers.add_parser('build')
    generator_parser = subparsers.add_parser('generate')
    help_parser = subparsers.add_parser('help')
    BuilderParser.add_arguments(builder_parser)
    GeneratorParser.add_arguments(generator_parser)
    args = parser.parse_args()
    # builder_ = NuitkaBuilder(args.config_path, args.main)
    # if args.dry_run: print(builder_.argv)
    # else: builder_.run()


if __name__ == '__main__': main()
