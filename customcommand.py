import inspect
import os.path
import re
import sys
import textwrap
import types
import warnings

from prettyprint import error, warn

registered = []
filename = os.path.basename(inspect.getfile(sys.modules["__main__"]))


def command(func: types.FunctionType):
    signature = inspect.signature(func)

    parameters = list(signature.parameters.values())
    if func.__doc__ is not None:
        doc = re.sub("\n *", " ", func.__doc__)
        doc = "\n        ".join(textwrap.wrap(doc))  # Reformat the docstring
    else:
        doc = ""

    required_arg_count = 0
    for arg in parameters:
        if arg.default is arg.empty:
            required_arg_count += 1
        if isinstance(arg.annotation, types.UnionType):
            warnings.warn("Custom Command doesn't support UnionType. Arguments will be converted into strings.")

        if not (arg.annotation is str or arg.annotation is int or arg.annotation is float or arg.annotation is arg.empty):
            warnings.warn(f"Custom Command doesn't support {arg.annotation.__name__}. "
                          f"Arguments will be converted into strings.")

    registered.append(
        {
            "name": func.__name__[0:-1] if func.__name__.endswith("_") else func.__name__,
            "parameters": parameters,
            "doc": doc,
            "function": func,
            "required_arg_count": required_arg_count
        }
    )

    return func

@command
def help_():
    """Show this help. List all the commands."""
    for i in registered:
        print(f"python {filename} {i['name']}:")
        print(f"    Doc:\n        {i['doc']}")
        print("    Arguments:" if i["parameters"] else "    No argument required.")
        for arg in i["parameters"]:
            if isinstance(arg.annotation, types.UnionType):
                t = str(arg.annotation)
            elif arg.annotation is arg.empty:
                t = "str"
            else:
                t = arg.annotation.__name__
            kind = "Required" if arg.default is arg.empty else "Optional"
            print(f"        {kind} - {arg.name}: {t} (can be used as -{arg.name})")
        print("    Positional Syntax: ", end="")
        for arg in i["parameters"]:
            print(f"<{arg.name}>" if arg.default is arg.empty else f"[{arg.name}]", end=" ")
        print("\n    Keyword Syntax: ", end="")
        for arg in i["parameters"]:
            print(f"-{arg.name} <value>", end=" ")
        print("\n")


def handle_commands():
    if len(sys.argv) < 2:
        error(f"Missing argument! See 'python {filename} help' for help.")
        return

    cmd_name = sys.argv[1]
    args = sys.argv[2:]

    for i in registered:
        if i["name"] == cmd_name:
            parameters = i["parameters"]
            required_count = i["required_arg_count"]

            pos_args = []
            kw_args = {}
            param_names = {p.name for p in parameters}
            skip_next = False
            
            for idx, arg in enumerate(args):
                if skip_next:
                    skip_next = False
                    continue
                if arg.startswith("-"):
                    if idx + 1 >= len(args):
                        error(f"Missing value for keyword argument '{arg}'.")
                        return
                    kw_name = arg[1:]
                    kw_args[kw_name] = args[idx + 1]
                    skip_next = True
                else:
                    pos_args.append(arg)

            for key in kw_args:
                if key not in param_names:
                    warn(f"Unknown keyword argument '-{key}'.")
            
            if len(pos_args) > len(parameters):
                error(f"Too many positional arguments! See 'python {filename} help' for help.")
                return

            if len(pos_args) < required_count:
                missing = parameters[len(pos_args)].name
                error(f"Missing argument '{missing}'! See 'python {filename} help' for help.")
                return

            final_args = []
            final_kwargs = {}

            for idx, param in enumerate(parameters):
                if idx < len(pos_args):
                    value = pos_args[idx]
                elif param.name in kw_args:
                    value = kw_args[param.name]
                elif param.default is not param.empty:
                    continue  # will use default
                else:
                    error(f"Missing required argument '{param.name}'!")
                    return

                try:
                    if param.annotation is int:
                        value = int(value)
                    elif param.annotation is float:
                        value = float(value)
                    # Leave as string or default
                except ValueError:
                    error(f"Invalid type for '{param.name}' argument! "
                          f"Expected '{param.annotation.__name__}'.")
                    return

                if idx < len(pos_args):
                    final_args.append(value)
                else:
                    final_kwargs[param.name] = value

            i["function"](*final_args, **final_kwargs)
            return

    error(f"Unknown command '{cmd_name}'! See 'python {filename} help' for help.")

"""
def handle_commands():
    if len(sys.argv) < 2:
        error(f"Missing argument! See `python {filename} help` for help.")
        return
    for i in registered:
        if i["name"] == sys.argv[1]:
            if len(sys.argv)-2 > len(i["parameters"]):
                error(f"Too many arguments! See `python {filename} help` for help.")
            elif len(sys.argv)-2 < i["required_arg_count"]:
                error(f"Missing argument `{i['parameters'][len(sys.argv)-2]}`! See `python {filename} help` for help.")
            else:
                converted = []
                for arg in range(len(sys.argv)-2):
                    try:
                        if i["parameters"][arg].annotation is int:
                            converted.append(int(sys.argv[2 + arg]))
                        elif i["parameters"][arg].annotation is float:
                            converted.append(float(sys.argv[2 + arg]))
                        else:
                            converted.append(sys.argv[2 + arg])
                    except ValueError:
                        error(f"Invalid type for `{i['parameters'][arg].name}` argument! "
                                    f"`{i['parameters'][arg].name}` argument must be type "
                                    f"`{i['parameters'][arg].annotation.__name__}`.")
                        return
                i["function"](*converted)
            return
    error(f"Unknown argument `{sys.argv[2]}`! See `python {filename} help` for help.")
"""
