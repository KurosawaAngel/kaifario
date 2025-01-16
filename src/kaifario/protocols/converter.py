from typing import Protocol


class KeyConverter(Protocol):
    def __call__(self, key: str) -> str: ...
