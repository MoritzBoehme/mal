from typing import Callable

import mal_types


def pr_str(mal: mal_types.MALType, print_readably: bool) -> str:
    match mal:
        case mal_types.MALList(elements):
            return (
                f"({' '.join(pr_str(element, print_readably) for element in elements)})"
            )
        case mal_types.MALSymbol(symbol):
            return symbol
        case mal_types.MALInt(value):
            return str(value)
        case mal_types.MALString(value):
            if print_readably:
                return f'"{unsecape(value)}"'
            else:
                return value
        case mal_types.MALNil():
            return "nil"
        case mal_types.MALVector(elements):
            return (
                f"[{' '.join(pr_str(element, print_readably) for element in elements)}]"
            )
        case mal_types.MALHash(mapping):
            pairs = (
                f"{pr_str(k, print_readably)} {pr_str(v, print_readably)}"
                for k, v in mapping.items()
            )
            return f"{{{' '.join(pairs)}}}"
        case mal_types.MALBool.TRUE | mal_types.MALBool.FALSE:
            return str(mal)
        case func if isinstance(func, (Callable, mal_types.MALFunction)):
            return "#<function>"
        case mal_types.MALAtom(value=value):
            return f"(atom {pr_str(value, print_readably)})"
        case _:
            raise RuntimeError(f"Cannot print type: {type(mal)}!")


def unsecape(string: str) -> str:
    backslash = string.replace("\\", "\\\\")
    quotes = backslash.replace('"', '\\"')
    newline = quotes.replace("\n", "\\n")
    return newline
