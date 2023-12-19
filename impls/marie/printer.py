from mal_types import MALType, MALList, MALInt, MALSymbol, MALString, MALNil, MALVector

def pr_str(mal: MALType, print_readably: bool) -> str:
    if isinstance(mal, MALList):
        return f"({' '.join(pr_str(m, print_readably) for m in mal)})"
    elif isinstance(mal, MALSymbol):
        return str(mal)
    elif isinstance(mal, MALInt):
        return str(mal)
    elif isinstance(mal, MALString):
        if print_readably:
            string = unsecape(mal)
        else:
            string = mal
        return f"\"{string}\""
    elif isinstance(mal, MALNil):
        return "nil"
    elif isinstance(mal, MALVector):
        return f"[{' '.join(pr_str(m, print_readably) for m in mal)}]"
    else:
        raise RuntimeError(f"Cannot print type: {type(mal)}!")

def unsecape(string: str) -> str:
    backslash = string.replace("\\", "\\\\")
    quotes = backslash.replace('"','\\"')
    newline = quotes.replace("\n", "\\\\n")
    return newline
