import reader
import printer
from mal_types import MALType

def READ(arg: str):
    return reader.read_str(arg)

def EVAL(arg: MALType):
    return arg

def PRINT(arg: MALType):
    return printer.pr_str(arg)

def rep(arg: str):
    r = READ(arg)
    e = EVAL(r)
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
