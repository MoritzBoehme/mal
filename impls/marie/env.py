from typing import Self

class Env:
    def __init__(self, outer: Self | None = None):
        self.data = {}
        self.outer = outer

    def __setitem__(self, k, v):
        self.data[k] = v

    def __getitem__(self, k):
        return self.find(k).data[k]

    def find(self, k):
        if self.data.get(k) is None:
            if self.outer is not None:
                return self.outer.find(k)
            else:
                raise Exception(f"{k} not found")
        else:
            return self
