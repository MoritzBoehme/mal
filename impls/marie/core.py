from typing import Callable

import printer
import reader
from mal_types import (
    MALAtom,
    MALBool,
    MALFunction,
    MALInt,
    MALList,
    MALNil,
    MALString,
    MALType,
    MALVector,
)


def eq(a: int, b: int, *args):
    return MALBool.from_bool(a == b)


def lt(a: int, b: int, *args):
    return MALBool.from_bool(a < b)


def le(a: int, b: int, *args):
    return MALBool.from_bool(a <= b)


def gt(a: int, b: int, *args):
    return MALBool.from_bool(a > b)


def ge(a: int, b: int, *args):
    return MALBool.from_bool(a >= b)


def _list(*args):
    return MALList(list(args))


def is_list(lst: MALType, *args):
    return MALBool.from_bool(isinstance(lst, MALList))


def is_empty(lst: MALList, *args):
    return MALBool.from_bool(len(lst) == 0)


def count(lst: MALList, *args):
    return MALInt(len(lst))


def _pr_str(*args):
    return MALString(" ".join(printer.pr_str(arg, True) for arg in args))


def _str(*args):
    return MALString("".join(printer.pr_str(arg, False) for arg in args))


def prn(*args):
    print(" ".join(printer.pr_str(arg, True) for arg in args))
    return MALNil()


def println(*args):
    print(" ".join(printer.pr_str(arg, False) for arg in args))
    return MALNil()


def slurp(filename):
    with open(filename.value, "r") as f:
        contents = f.read()
    return MALString(contents)


def is_atom(atom: MALAtom):
    return MALBool.from_bool(isinstance(atom, MALAtom))


def deref(atom: MALAtom):
    return atom.value


def reset(atom: MALAtom, value: MALType):
    atom.value = value
    return value


def swap(atom: MALAtom, func: MALFunction | Callable, *args):
    result = func(atom.value, *args)
    return reset(atom, result)


def cons(arg: MALType, lst: MALList):
    return concat(MALList([arg]), lst)


def concat(*args):
    final = []
    for lst in args:
        final += lst.value
    return MALList(final)


def atom(value):
    return MALAtom(value)

def nth(lst: MALList | MALVector, i: MALInt) -> MALType:
    return lst[i.value]

def first(xs: MALList | MALVector | MALNil) -> MALType:
    if isinstance(xs, MALNil) or len(xs) == 0:
        return MALNil()
    return xs[0]

def rest(xs: MALList | MALVector | MALNil) -> MALVector:
    if isinstance(xs, MALNil) or len(xs) == 0:
        return MALList([])
    return MALList(xs[1:])

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
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "read-string": lambda a: reader.read_str(a.value),
    "slurp": slurp,
    "atom": atom,
    "atom?": is_atom,
    "deref": deref,
    "reset!": reset,
    "swap!": swap,
    "cons": cons,
    "concat": concat,
    "vec": lambda lst: MALVector(lst.value),
    "nth": nth,
    "first": first,
    "rest": rest,
}
