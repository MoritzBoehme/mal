from typing import Callable
try:
    from itertools import batched
except ImportError:
    from itertools import islice

    def batched(iterable, n):
        # batched('ABCDEFG', 3) → ABC DEF G
        if n < 1:
            raise ValueError('n must be at least one')
        iterator = iter(iterable)
        while batch := tuple(islice(iterator, n)):
            yield batch

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
    MALException,
    MALSymbol,
    MALKeyword,
    MALHash,
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
    try:
        return lst[i.value]
    except IndexError as e:
        raise MALException(MALString(str(e)))

def first(xs: MALList | MALVector | MALNil) -> MALType:
    if isinstance(xs, MALNil) or len(xs) == 0:
        return MALNil()
    return xs[0]

def rest(xs: MALList | MALVector | MALNil) -> MALVector:
    if isinstance(xs, MALNil) or len(xs) == 0:
        return MALList([])
    return MALList(xs[1:])

def throw(value: MALType):
    raise MALException(value)

def apply(func: MALFunction, *args: MALType):
    head, last = args[:-1], args[-1]
    result = func(*head, *last.value)
    return result

def map_(func: MALFunction, args: MALList[MALType]):
    results = [func(arg) for arg in args.value]
    return MALList(results)

def is_nil(arg: MALType) -> MALBool:
    return MALBool.from_bool(isinstance(arg, MALNil))

def is_true(arg: MALType) -> MALBool:
    return MALBool.from_bool(arg == MALBool.TRUE)

def is_false(arg: MALType) -> MALBool:
    return MALBool.from_bool(arg == MALBool.FALSE)

def is_symbol(arg: MALType) -> MALBool:
    return MALBool.from_bool(isinstance(arg, MALSymbol))

def symbol(arg: MALString) -> MALSymbol:
    return MALSymbol(arg.value)

def keyword(arg: MALString | MALKeyword) -> MALKeyword:
    if isinstance(arg, MALKeyword):
        return arg
    else:
        return MALKeyword(arg.value)

def is_keyword(arg: MALType) -> MALBool:
    return MALBool.from_bool(isinstance(arg, MALKeyword))

def vector(*args: tuple[MALType]) -> MALVector:
    return MALVector(list(args))

def is_vector(arg: MALType) -> MALBool:
    return MALBool.from_bool(isinstance(arg, MALVector))

def is_sequential(arg: MALType) -> MALBool:
    return MALBool.from_bool(isinstance(arg, MALList | MALVector))

def hash_map(*args: tuple[MALType]) -> MALHash:
    mapping = {}
    for pair in batched(args, 2):
        if len(pair) < 2:
            raise MALException(MALString(f"Key without value {pair[0]}"))
        mapping[pair[0]] = pair[1]
    return MALHash(mapping)

def is_map(arg: MALType) -> MALBool:
    return MALBool.from_bool(isinstance(arg, MALHash))

def assoc(map_: MALHash, *args: tuple[MALType]) -> MALHash:
    other_map = hash_map(*args)
    return MALHash({**map_.value, **other_map.value})

def dissoc(map_: MALHash, *args: tuple[MALType]) -> MALHash:
    to_remove = set(args)
    new_map = {}
    for k, v in map_.value.items():
        if k not in to_remove:
            new_map[k] = v

    return MALHash(new_map)

def get(map_: MALHash | MALNil, key: MALType) -> MALType:
    if isinstance(map_, MALNil):
        return MALNil()
    return map_.value.get(key, MALNil())

def contains(map_: MALHash, key: MALType) -> MALBool:
    return MALBool.from_bool(key in map_.value)

def keys(map_: MALHash) -> MALList[MALType]:
    return MALList(list(map_.value.keys()))

def vals(map_: MALHash) -> MALList[MALType]:
    return MALList(list(map_.value.values()))

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
    "throw": throw,
    "apply": apply,
    "map": map_,
    "nil?": is_nil,
    "true?": is_true,
    "false?": is_false,
    "symbol?": is_symbol,
    "symbol": symbol,
    "keyword": keyword,
    "keyword?": is_keyword,
    "vector": vector,
    "vector?": is_vector,
    "sequential?": is_sequential,
    "hash-map": hash_map,
    "map?": is_map,
    "assoc": assoc,
    "dissoc": dissoc,
    "get": get,
    "contains?": contains,
    "keys": keys,
    "vals": vals,
}
