from enum import StrEnum
from typing import Self, Union, Callable


class MALList(list):
    pass


class MALVector(list):
    pass


class MALInt(int):
    pass


class MALSymbol(str):
    pass


class MALString(str):
    pass


class MALNil:
    def __len__(self):
        return 0

    def __eq__(self, other):
        return isinstance(other, MALNil)


class MALHash(dict):
    pass


class MALBool(StrEnum):
    TRUE = "true"
    FALSE = "false"

    def __bool__(self):
        return self == MALBool.TRUE

    @classmethod
    def from_bool(cls: Self, b: bool):
        if b:
            return cls.TRUE
        else:
            return cls.FALSE

SimpleMALType = Union[
    MALList, MALVector, MALInt, MALSymbol, MALString, MALNil, MALHash, MALBool
]

class MALAtom:
    def __init__(self, value: SimpleMALType):
        self.value = value

class MALFunction:
    def __init__(
            self, ast: SimpleMALType, params: list[MALSymbol], env: "Env", eval: Callable | None = None,
    ):
        self.ast = ast
        self.params = params
        self.env = env

        def fn(*args):
            # HACK: because we cannot import the Env class
            fn_env = type(env)(env, params, list(args))
            return eval(ast, fn_env)
        self.fn = fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


MALType = SimpleMALType | MALAtom | MALFunction
