import reader
import printer
from mal_types import MALType, MALEnv, MALSymbol, MALList, MALInt

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
            evaluated = eval_ast(ast, env)
            return evaluated[0](*evaluated[1:])
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
            raise Exception("symbol not found")
        return symb
    elif isinstance(ast, MALList):
        return MALList([EVAL(sub, env) for sub in ast])
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
