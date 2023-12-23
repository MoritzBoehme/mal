from typing import Callable

import printer
import reader
from mal_types import MALHash, MALList, MALSymbol, MALType, MALVector

MALEnv = dict[str, Callable]
repl_env: MALEnv = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def READ(arg: str):
    return reader.read_str(arg)


def EVAL(ast: MALType, env: MALEnv):
    match ast:
        case MALList(elements):
            if len(elements) > 0:
                f, *args = eval_ast(ast, env).value
                return f(*args)
            else:
                return ast
        case _:
            return eval_ast(ast, env)


def PRINT(arg: MALType):
    return printer.pr_str(arg, print_readably=True)


def eval_ast(ast: MALType, env: MALEnv):
    match ast:
        case MALSymbol(name):
            symb = env.get(name)
            if symb is None:
                raise Exception(f"{name} not found")
            return symb
        case MALList(elements):
            return MALList([EVAL(element, env) for element in elements])
        case MALVector(elements):
            return MALVector([EVAL(element, env) for element in elements])
        case MALHash(mapping):
            return MALHash({k: EVAL(v, env) for k, v in mapping.items()})
        case _:
            return ast


def rep(arg: str):
    r = READ(arg)
    e = EVAL(r, repl_env)
    p = PRINT(e)
    return p


if __name__ == "__main__":
    while True:
        try:
            inp = input("user> ")
        except EOFError:
            break
        try:
            r = rep(inp)
        except Exception as e:
            print(e)
        else:
            print(r)
