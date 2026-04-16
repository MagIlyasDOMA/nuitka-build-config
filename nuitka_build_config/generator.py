import argparse
from typing import Callable, Any, Union
from pathlib import Path
from .argv_add_method import ArgvAddMethod
from .builder import NuitkaBuilder
from .typings import FieldType


class NuitkaParser(argparse.ArgumentParser):
    groups: dict

    def add_arguments(self):
        for method in NuitkaBuilder.add_argv_methods():
            if method.field_type == 'custom': continue
            elif method.field_type == 'choice':
                group = self.add_mutually_exclusive_group()
                self.groups[method.field_name] = group
                for value, flag in method.type_data.items():
                    group.add_argument(flag, action='store_const', const=value,
                                       dest=method.field_name)
            elif method.field_type == 'ternary':
                group = self.add_mutually_exclusive_group()
                self.groups[method.field_name] = group
                group.add_argument(method.type_data['true'], action='store_const', const=True,
                                   dest=method.field_name)
                group.add_argument(method.type_data['false'], action='store_const', const=False,
                                   dest=method.field_name)
            else:
                data = dict(dest=method.field_name)
                match method.field_type:
                    case 'str': data['type'] = str
                    case 'int': data['type'] = int
                    case 'bool': data['action'] = 'store_true'
                    case 'pathlike': data['type'] = Path
                    case 'strlist': data.update(action='append', type=str)
                    case 'filelist': data.update(action='append', type=Path)
                self.add_argument(method.flag, **data)

