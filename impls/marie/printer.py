from mal_types import MALType, MALList, MALInt, MALSymbol, MALString, MALNil

def pr_str(mal: MALType) -> str:
    if isinstance(mal, MALList):
        return f"({' '.join(pr_str(m) for m in mal)})"
    elif isinstance(mal, MALSymbol):
        return str(mal)
    elif isinstance(mal, MALInt):
        return str(mal)
    elif isinstance(mal, MALString):
        return str(mal)
    elif isinstance(mal, MALNil):
        return "nil"
