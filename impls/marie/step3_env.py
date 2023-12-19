import reader
import printer
from mal_types import MALType, MALSymbol, MALList, MALInt, MALVector, MALHash
from env import Env

repl_env = Env()
repl_env["+"] = lambda a, b: MALInt(a + b)
repl_env["-"] = lambda a, b: MALInt(a - b)
repl_env["*"] = lambda a, b: MALInt(a * b)
repl_env["/"] = lambda a, b: MALInt(a / b)


def READ(arg: str):
    return reader.read_str(arg)


def EVAL(ast: MALType, env: Env):
    if not isinstance(ast, MALList):
        return eval_ast(ast, env)
    elif len(ast) == 0:
        return ast
    match ast[0]:
        case "def!":
            v = EVAL(ast[2], env)
            env[ast[1]] = v
            return v
        case "let*":
            let_env = Env(env)
            for k, v in zip(ast[1][:-1:2], ast[1][1::2]):
                let_env[k] = EVAL(v, let_env)
            return EVAL(ast[2], let_env)
        case _:
            f, *args = eval_ast(ast, env)
            return f(*args)


def PRINT(arg: MALType):
    return printer.pr_str(arg, print_readably=True)


def eval_ast(ast: MALType, env: Env):
    if isinstance(ast, MALSymbol):
        return env[ast]
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
