from typing import Union, Any
from enum import StrEnum

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
    pass

class MALHash(dict):
    pass

class MALBool(StrEnum):
    TRUE = "true"
    FALSE = "false"

MALType = Union[MALList, MALVector, MALInt, MALSymbol, MALString, MALNil, MALHash]
MALEnv = dict[str, Any]
