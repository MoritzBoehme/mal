from typing import Union, Any

class MALList(list):
    pass

class MALInt(int):
    pass

class MALSymbol(str):
    pass

class MALString(str):
    pass

class MALNil:
    pass

MALType = Union[MALList, MALInt, MALSymbol]
MALEnv = dict[str, Any]
