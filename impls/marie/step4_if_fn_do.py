import core
import mal_types
import printer
import reader
from env import Env

repl_env = Env()
for k, v in core.ns.items():
    repl_env[k] = v


def READ(arg: str):
    return reader.read_str(arg)


def EVAL(ast: mal_types.MALType, env: Env):
    if not isinstance(ast, mal_types.MALList):
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
        case "do":
            for sub in ast[1:]:
                last = EVAL(sub, env)
            return last
        case "if":
            condition = EVAL(ast[1], env)
            if (
                not isinstance(condition, mal_types.MALNil)
                and condition != mal_types.MALBool.FALSE
            ):
                return EVAL(ast[2], env)
            else:
                if len(ast) > 3:
                    return EVAL(ast[3], env)
                else:
                    return mal_types.MALNil()
        case "fn*":

            def closure(*args):
                fn_env = Env(env, binds=ast[1], exprs=list(args))
                return EVAL(ast[2], fn_env)

            return closure
        case _:
            f, *args = eval_ast(ast, env)
            return f(*args)


def PRINT(arg: mal_types.MALType):
    return printer.pr_str(arg, print_readably=True)


def eval_ast(ast: mal_types.MALType, env: Env):
    if isinstance(ast, mal_types.MALSymbol):
        return env[ast]
    elif isinstance(ast, mal_types.MALList):
        return mal_types.MALList([EVAL(sub, env) for sub in ast])
    elif isinstance(ast, mal_types.MALVector):
        return mal_types.MALVector([EVAL(sub, env) for sub in ast])
    elif isinstance(ast, mal_types.MALHash):
        return mal_types.MALHash({k: EVAL(v, env) for k, v in ast.items()})
    else:
        return ast


def rep(arg: str):
    r = READ(arg)
    e = EVAL(r, repl_env)
    p = PRINT(e)
    return p


rep("(def! not (fn* (a) (if a false true)))")

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
