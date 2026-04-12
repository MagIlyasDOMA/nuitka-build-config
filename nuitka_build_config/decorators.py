from .typings import ArgvAddMethod, ArgType, StrList, ArgvAddStrMethod, NullStr


def argv_add(method: ArgvAddMethod) -> ArgvAddMethod:
    def new_method(self, argv: StrList, arg: ArgType):
        data = method(self, argv, arg)
        argv.extend(data)
        return data
    new_method.argv_add = True
    new_method.config_attr_type = 'argv_add'
    return new_method
