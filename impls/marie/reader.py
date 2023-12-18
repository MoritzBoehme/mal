import re
from mal_types import MALList, MALType, MALSymbol, MALInt, MALString, MALNil

REGEX = r"[\s,]*(~@|[\[\]{}()'`~^@]|\"(?:\\.|[^\\\"])*\"?|;.*|[^\s\[\]{}('\"`,;)]*)"
COMPILED = re.compile(REGEX)


class Reader:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.position = 0

    def next(self):
        tok = self.tokens[self.position]
        self.position += 1
        return tok

    def peek(self):
        return self.tokens[self.position]


def read_str(string: str) -> MALType:
    tokens = tokenize(string)
    reader = Reader(tokens)
    return read_form(reader)


def tokenize(string: str) -> list[str]:
    return COMPILED.findall(string)


def read_form(reader: Reader) -> MALType:
    if reader.peek() == "(":
        return read_list(reader)
    else:
        return read_atom(reader)


def read_list(reader: Reader) -> MALList:
    reader.next()  # skip (
    mal_list = []
    try:
        while not (tok := read_form(reader)) == ")":
            mal_list.append(tok)
    except Exception:
        raise Exception("EOF")
    return MALList(mal_list)


def read_atom(reader: Reader):
    tok = reader.next()
    try:
        return MALInt(tok)
    except Exception:
        pass

    if tok.startswith('"'):
        return MALString(tok)

    if tok == "nil":
        return MALNil()

    return MALSymbol(tok)
