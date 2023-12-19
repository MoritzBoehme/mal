from enum import StrEnum
from typing import Any, Self, Union


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


MALType = Union[
    MALList, MALVector, MALInt, MALSymbol, MALString, MALNil, MALHash, MALBool
]
MALEnv = dict[str, Any]
