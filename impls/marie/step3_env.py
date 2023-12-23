import printer
import reader
from env import Env
from mal_types import MALContainer, MALHash, MALList, MALSymbol, MALType, MALVector

repl_env = Env()
repl_env["+"] = lambda a, b: a + b
repl_env["-"] = lambda a, b: a - b
repl_env["*"] = lambda a, b: a * b
repl_env["/"] = lambda a, b: a / b


def READ(arg: str):
    return reader.read_str(arg)


def EVAL(ast: MALType, env: Env):
    match ast:
        case MALContainer([]):
            return ast
        case MALList([MALSymbol("def!"), MALSymbol(name), value]):
            v = EVAL(value, env)
            env[name] = v
            return v
        case MALList([MALSymbol("let*"), MALContainer(assignments), expr]):
            let_env = Env(env)
            for k, v in zip(assignments[:-1:2], assignments[1::2]):
                let_env[k.value] = EVAL(v, let_env)
            return EVAL(expr, let_env)
        case MALList(_):
            value = eval_ast(ast, env).value
            f, *args = value
            return f(*args)
        case _:
            return eval_ast(ast, env)


def PRINT(arg: MALType):
    return printer.pr_str(arg, print_readably=True)


def eval_ast(ast: MALType, env: Env):
    match ast:
        case MALSymbol(_):
            return env[ast.value]
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
