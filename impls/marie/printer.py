import mal_types

def pr_str(mal: mal_types.MALType, print_readably: bool) -> str:
    if isinstance(mal, mal_types.MALList):
        return f"({' '.join(pr_str(m, print_readably) for m in mal)})"
    elif isinstance(mal, mal_types.MALSymbol):
        return str(mal)
    elif isinstance(mal, mal_types.MALInt):
        return str(mal)
    elif isinstance(mal, mal_types.MALString):
        if print_readably:
            string = unsecape(mal)
        else:
            string = mal
        return f"\"{string}\""
    elif isinstance(mal, mal_types.MALNil):
        return "nil"
    elif isinstance(mal, mal_types.MALVector):
        return f"[{' '.join(pr_str(m, print_readably) for m in mal)}]"
    elif isinstance(mal, mal_types.MALHash):
        pairs = (f"{pr_str(k, print_readably)} {pr_str(v, print_readably)}" for k, v in mal.items())
        return f"{{{' '.join(pairs)}}}"
    else:
        raise RuntimeError(f"Cannot print type: {type(mal)}!")

def unsecape(string: str) -> str:
    backslash = string.replace("\\", "\\\\")
    quotes = backslash.replace('"','\\"')
    newline = quotes.replace("\n", "\\\\n")
    return newline
