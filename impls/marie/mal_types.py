from enum import StrEnum
from typing import Callable, NamedTuple, Self, Union
import printer


class MALContainer(NamedTuple):
    value: list["MALType"]

    def __len__(self):
        return len(self.value)

    def __getitem__(self, idx):
        return self.value[idx]

    def __eq__(self, other):
        if isinstance(other, MALContainer):
            return self.value == other.value
        return False


class MALList(MALContainer):
    pass


class MALVector(MALContainer):
    pass


class MALInt(NamedTuple):
    value: int

    def __add__(self, other) -> Self:
        return MALInt(self.value + other.value)

    def __mul__(self, other) -> Self:
        return MALInt(self.value * other.value)

    def __truediv__(self, other) -> Self:
        return MALInt(self.value / other.value)

    def __sub__(self, other) -> Self:
        return MALInt(self.value - other.value)


class MALSymbol(NamedTuple):
    value: str

    def __eq__(self, other):
        if isinstance(other, MALSymbol):
            return self.value == other.value
        return False


class MALString(NamedTuple):
    value: str

    def __eq__(self, other):
        if isinstance(other, MALString):
            return self.value == other.value
        return False


class MALNil(NamedTuple):
    pass


class MALHash(NamedTuple):
    value: dict["MALType", "MALType"]


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

class MALKeyword(NamedTuple):
    value: str


SimpleMALType = Union[
    MALList, MALVector, MALInt, MALSymbol, MALString, MALNil, MALHash, MALBool, MALKeyword
]


class MALAtom:
    def __init__(self, value: SimpleMALType):
        self.value = value


class MALFunction:
    def __init__(
        self,
        ast: SimpleMALType,
        params: list[MALSymbol],
        env: "Env",
        eval: Callable | None = None,
    ):
        self.ast = ast
        self.params = params
        self.env = env
        self.is_macro = False

        def fn(*args):
            # HACK: because we cannot import the Env class
            fn_env = type(env)(env, params, list(args))
            return eval(ast, fn_env)

        self.fn = fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


MALType = SimpleMALType | MALAtom | MALFunction


class MALException(Exception):
    def __init__(self, value: MALType):

        message = f"Exception: {printer.pr_str(value, print_readably=True)}"
        super().__init__(message)
        self.value = value
