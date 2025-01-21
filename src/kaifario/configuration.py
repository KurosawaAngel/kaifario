from typing import Any, TypeVar

from adaptix import Retort

from kaifario.protocols import Loader

T = TypeVar("T")


class Configuration:
    def __init__(
        self,
        data: dict[str, Any],
        loader: Loader | None = None,
    ) -> None:
        self._data = data
        if loader is None:
            self._loader = Retort(strict_coercion=False)

    def get_section(self, key: str) -> "Configuration":
        return Configuration(self._data.get(key, {}), self._loader)

    def __getitem__(self, key: str) -> "Configuration":
        return self.get_section(key)

    def get(self, t: type[T]) -> T:
        return self._loader.load(self._data, t)

    def get_value(self, key: str, t: type[T]) -> T:
        return self._loader.load(self._data[key], t)
