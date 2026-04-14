import argparse
from pathlib import Path
from .builder import NuitkaBuilder
from .models import NuitkaConfig
from .typings.models import NuitkaConfigDict

__all__ = ['NuitkaBuilder', 'NuitkaConfig', 'NuitkaConfigDict', 'main']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path', type=Path, help='Path to Nuitka config file',
                        nargs='?', default=None)
    parser.add_argument('main', type=Path, help='Path to main Nuitka build file',
                        nargs='?', default=None)
    args = parser.parse_args()
    NuitkaBuilder(**vars(args)).run()


if __name__ == '__main__': main()
