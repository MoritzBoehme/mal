import sys

def READ(arg: str):
    return arg

def EVAL(arg: str):
    return arg

def PRINT(arg: str):
    return arg

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
        r = rep(inp)
        print(r)
