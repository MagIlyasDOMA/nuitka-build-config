from argparse_help_i18n import HelpI18nMixin
from scparser import *

__all__ = ['MainParser', 'NBCSubcommandsAction']


class NBCSubcommandsAction(SubcommandsAction):
    def add_parser(self, name: str, *, parser: ParserType = None, **kwargs):
        kwargs.setdefault('add_version', False)
        return super().add_parser(name, parser=parser, **kwargs)


class MainParser(SubcommandsParser, HelpI18nMixin):
    def add_subparsers(self, **kwargs):
        kwargs.setdefault('action', 'nbc_subcmds')
        self.register('action', 'nbc_subcmds', SubcommandsAction)
        return super().add_subparsers(**kwargs)
