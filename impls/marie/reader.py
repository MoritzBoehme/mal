import re

from mal_types import MALInt, MALList, MALNil, MALString, MALSymbol, MALType, MALVector

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
    match reader.peek():
        case "(":
            return read_list(reader, end=")", type_class=MALList)
        case "[":
            return read_list(reader, end="]", type_class=MALVector)
        case _:
            return read_atom(reader)


def read_list(reader: Reader, end: str, type_class: type) -> MALList:
    reader.next()  # skip (
    mal_list = []
    try:
        while not (tok := read_form(reader)) == end:
            mal_list.append(tok)
    except Exception:
        raise Exception("unbalanced parens")
    return type_class(mal_list)


def read_atom(reader: Reader):
    tok = reader.next()
    try:
        return MALInt(tok)
    except Exception:
        pass

    if tok.startswith('"'):
        return MALString(escape_string(tok))

    if tok == "nil":
        return MALNil()

    return MALSymbol(tok)


def escape_string(tok: str) -> MALString:
    reader = Reader(list(tok))
    reader.next()  # skip "
    string = []
    try:
        while not (tok := reader.peek()) == '"':
            if tok == "\\":
                reader.next()
                next_tok = reader.peek()
                if next_tok == "\\":
                    string.append("\\")
                elif next_tok == "n":
                    string.append("\n")
                elif next_tok == '"':
                    string.append('"')
                reader.next()
            else:
                string.append(reader.next())
    except Exception:
        raise Exception("unbalanced double quotes")
    return "".join(string)
