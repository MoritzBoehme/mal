import mal_types
from typing import Callable

def pr_str(mal: mal_types.MALType, print_readably: bool) -> str:
    if isinstance(mal, mal_types.MALList):
        return f"({' '.join(pr_str(m, print_readably) for m in mal)})"
    elif isinstance(mal, mal_types.MALSymbol):
        return str(mal)
    elif isinstance(mal, mal_types.MALInt):
        return str(mal)
    elif isinstance(mal, mal_types.MALString):
        if print_readably:
            return f"\"{unsecape(mal)}\""
        else:
            return mal
    elif isinstance(mal, mal_types.MALNil):
        return "nil"
    elif isinstance(mal, mal_types.MALVector):
        return f"[{' '.join(pr_str(m, print_readably) for m in mal)}]"
    elif isinstance(mal, mal_types.MALHash):
        pairs = (f"{pr_str(k, print_readably)} {pr_str(v, print_readably)}" for k, v in mal.items())
        return f"{{{' '.join(pairs)}}}"
    elif isinstance(mal, mal_types.MALBool):
        return str(mal)
    elif isinstance(mal, Callable):
        return "#<function>"
    else:
        raise RuntimeError(f"Cannot print type: {type(mal)}!")

def unsecape(string: str) -> str:
    backslash = string.replace("\\", "\\\\")
    quotes = backslash.replace('"','\\"')
    newline = quotes.replace("\n", "\\n")
    return newline
