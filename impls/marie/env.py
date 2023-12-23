from typing import Any, Self

from mal_types import MALList, MALType


class Env:
    def __init__(
        self,
        outer: Self | None = None,
        binds: list[str] = [],
        exprs: list[MALType] = [],
    ):
        self.data = {}
        self.outer = outer
        for i, k in enumerate(binds):
            if k.value == "&":
                self[binds[i + 1].value] = MALList(exprs[i:])
                break
            else:
                self[k.value] = exprs[i]

    def __setitem__(self, k: str, v: MALType) -> Any:
        self.data[k] = v

    def __getitem__(self, k: str) -> MALType:
        return self.find(k).data[k]

    def find(self, k: str) -> Self:
        if self.data.get(k) is None:
            if self.outer is not None:
                return self.outer.find(k)
            else:
                raise Exception(f"{k!r} not found")
        else:
            return self
