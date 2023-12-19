from typing import Self, Any
from mal_types import MALType, MALList

class Env:
    def __init__(self, outer: Self | None = None, binds: list[MALType] = [], exprs: list[Any] = []):
        self.data = {}
        self.outer = outer
        for i, k in enumerate(binds):
            if k == "&":
                self[binds[i+1]] = MALList(exprs[i:])
                break
            else:
                self[k] = exprs[i]

    def __setitem__(self, k, v) -> Any:
        self.data[k] = v

    def __getitem__(self, k) -> Any:
        return self.find(k).data[k]

    def find(self, k) -> Self:
        if self.data.get(k) is None:
            if self.outer is not None:
                return self.outer.find(k)
            else:
                raise Exception(f"{k} not found")
        else:
            return self
