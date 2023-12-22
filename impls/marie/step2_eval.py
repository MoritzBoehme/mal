from typing import Callable

import printer
import reader
from mal_types import MALHash, MALInt, MALList, MALSymbol, MALType, MALVector

MALEnv = dict[str, Callable]
repl_env: MALEnv = {
    "+": lambda a, b: MALInt(a + b),
    "-": lambda a, b: MALInt(a - b),
    "*": lambda a, b: MALInt(a * b),
    "/": lambda a, b: MALInt(a / b),
}


def READ(arg: str):
    return reader.read_str(arg)


def EVAL(ast: MALType, env: MALEnv):
    if isinstance(ast, MALList):
        if len(ast) > 0:
            f, *args = eval_ast(ast, env)
            return f(*args)
        else:
            return ast
    else:
        return eval_ast(ast, env)


def PRINT(arg: MALType):
    return printer.pr_str(arg, print_readably=True)


def eval_ast(ast: MALType, env: MALEnv):
    if isinstance(ast, MALSymbol):
        symb = env.get(ast)
        if symb is None:
            raise Exception(f"{ast} not found")
        return symb
    elif isinstance(ast, MALList):
        return MALList([EVAL(sub, env) for sub in ast])
    elif isinstance(ast, MALVector):
        return MALVector([EVAL(sub, env) for sub in ast])
    elif isinstance(ast, MALHash):
        return MALHash({k: EVAL(v, env) for k, v in ast.items()})
    else:
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
