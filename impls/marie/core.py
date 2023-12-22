from typing import Callable

import mal_types
import printer
import reader


def eq(a: int, b: int, *args):
    return mal_types.MALBool.from_bool(a == b)


def lt(a: int, b: int, *args):
    return mal_types.MALBool.from_bool(a < b)


def le(a: int, b: int, *args):
    return mal_types.MALBool.from_bool(a <= b)


def gt(a: int, b: int, *args):
    return mal_types.MALBool.from_bool(a > b)


def ge(a: int, b: int, *args):
    return mal_types.MALBool.from_bool(a >= b)


def _list(*args):
    return mal_types.MALList(args)


def is_list(lst: mal_types.MALType, *args):
    return mal_types.MALBool.from_bool(isinstance(lst, mal_types.MALList))


def is_empty(lst: mal_types.MALList, *args):
    return mal_types.MALBool.from_bool(len(lst) == 0)


def count(lst: mal_types.MALList, *args):
    return mal_types.MALInt(len(lst))


def _pr_str(*args):
    return mal_types.MALString(" ".join(printer.pr_str(arg, True) for arg in args))


def _str(*args):
    return mal_types.MALString("".join(printer.pr_str(arg, False) for arg in args))


def prn(*args):
    print(" ".join(printer.pr_str(arg, True) for arg in args))
    return mal_types.MALNil()


def println(*args):
    print(" ".join(printer.pr_str(arg, False) for arg in args))
    return mal_types.MALNil()


def slurp(*args):
    with open(args[0], "r") as f:
        contents = f.read()
    return mal_types.MALString(contents)


def is_atom(atom: mal_types.MALAtom):
    return mal_types.MALBool.from_bool(isinstance(atom, mal_types.MALAtom))


def deref(atom: mal_types.MALAtom):
    return atom.value


def reset(atom: mal_types.MALAtom, value: mal_types.MALType):
    atom.value = value
    return value


def swap(atom: mal_types.MALAtom, func: mal_types.MALFunction | Callable, *args):
    result = func(atom.value, *args)
    return reset(atom, result)


ns = {
    "=": eq,
    "<": lt,
    "<=": le,
    ">": gt,
    ">=": ge,
    "list": _list,
    "list?": is_list,
    "empty?": is_empty,
    "count": count,
    "pr-str": _pr_str,
    "str": _str,
    "prn": prn,
    "println": println,
    "+": lambda a, b: mal_types.MALInt(a + b),
    "-": lambda a, b: mal_types.MALInt(a - b),
    "*": lambda a, b: mal_types.MALInt(a * b),
    "/": lambda a, b: mal_types.MALInt(a / b),
    "read-string": reader.read_str,
    "slurp": slurp,
    "atom": mal_types.MALAtom,
    "atom?": is_atom,
    "deref": deref,
    "reset!": reset,
    "swap!": swap,
}
