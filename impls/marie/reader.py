import re

import mal_types

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


def read_str(string: str) -> mal_types.MALType:
    tokens = tokenize(string)
    reader = Reader(tokens)
    return read_form(reader)


def tokenize(string: str) -> list[str]:
    tokens = COMPILED.findall(string)
    without_comments = [token for token in tokens if not token.startswith(";")]
    return without_comments


def read_hash(reader: Reader) -> mal_types.MALHash:
    reader.next()  # skip {
    mal_hash = {}
    try:
        while True:
            if reader.peek() == "}":
                reader.next()
                break
            key = read_form(reader)
            if reader.peek() == "}":
                raise Exception("key without value")
            value = read_form(reader)
            mal_hash[key] = value
    except IndexError:
        raise Exception("EOF")
    return mal_types.MALHash(mal_hash)


def read_list(
    reader: Reader, end: str, type_class: type
) -> mal_types.MALList | mal_types.MALVector:
    reader.next()  # skip starting char
    mal_list = []
    end_symbol = mal_types.MALSymbol(end)
    try:
        while not (tok := read_form(reader)) == end_symbol:
            mal_list.append(tok)
    except Exception:
        raise Exception("unbalanced parens")
    return type_class(mal_list)


def read_atom(reader: Reader):
    tok = reader.next()
    try:
        return mal_types.MALInt(int(tok))
    except Exception:
        pass

    if tok.startswith('"'):
        return escape_string(tok)

    if tok == "nil":
        return mal_types.MALNil()

    if tok == mal_types.MALBool.TRUE or tok == mal_types.MALBool.FALSE:
        return mal_types.MALBool(tok)

    return mal_types.MALSymbol(tok)


def escape_string(tok: str) -> mal_types.MALString:
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
    return mal_types.MALString("".join(string))


def read_form(reader: Reader) -> mal_types.MALType:
    match reader.peek():
        case "(":
            return read_list(reader, end=")", type_class=mal_types.MALList)
        case "[":
            return read_list(reader, end="]", type_class=mal_types.MALVector)
        case "{":
            return read_hash(reader)
        case "@":
            reader.next()  # skip "@"
            return mal_types.MALList(
                [mal_types.MALSymbol("deref")] + [read_form(reader)]
            )
        case "'":
            reader.next() # skip "'"
            return mal_types.MALList([mal_types.MALSymbol("quote"), read_form(reader)])
        case "`":
            reader.next() # skip "`"
            return mal_types.MALList([mal_types.MALSymbol("quasiquote"), read_form(reader)])
        case "~":
            reader.next() # skip "~"
            return mal_types.MALList([mal_types.MALSymbol("unquote"), read_form(reader)])
        case "~@":
            reader.next() # skip "~@"
            return mal_types.MALList([mal_types.MALSymbol("splice-unquote"), read_form(reader)])
        case _:
            return read_atom(reader)
