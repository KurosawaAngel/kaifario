import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any

from kaifario.protocols import ConfigurationProvider
from kaifario.protocols.converter import KeyConverter


class EnviromentProvider(ConfigurationProvider):
    def __init__(
        self,
        prefix: str = "",
        key_converter: KeyConverter | None = None,
    ) -> None:
        self.prefix = prefix
        if key_converter is None:
            key_converter = convert_snake_style
        self.key_converter = key_converter

    def _set_nested_value(
        self,
        data: dict[str, Any],
        keys: list[str],
        value: Any,
    ) -> None:
        current = data
        for key in keys[:-1]:
            key = self.key_converter(key)
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def load(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for env, value in os.environ.items():
            if env.startswith(self.prefix):
                s = env.removeprefix(self.prefix)
                keys = s.split("__")
                self._set_nested_value(data, keys, value)
        return data


ONLY_WORD_CHARS = re.compile(r"\w+")


def is_snake_style(name: str) -> bool:
    return ONLY_WORD_CHARS.fullmatch(name) is not None


SNAKE_SPLITTER = re.compile(r"(_*)([^_]+)(.*?)(_*)$")
REST_SUB = re.compile(r"(_+)|([^_]+)")


@dataclass
class StyleConversion:
    sep: str
    first: Callable[[str], str]
    other: Callable[[str], str]


def rest_sub(conv: StyleConversion, match_: re.Match):
    if match_[1] is None:
        return conv.other(match_[2])
    return match_[1].replace("_", conv.sep)


def convert_snake_style(key: str) -> str:
    if not is_snake_style(key):
        raise ValueError("Cannot convert a name that not follows snake style")

    match = SNAKE_SPLITTER.match(key)
    if match is None:
        raise ValueError(f"Cannot convert {key!r}")

    front_us, raw_first, raw_rest, trailing_us = match.groups()
    conv = StyleConversion("_", str.upper, str.upper)

    first = conv.first(raw_first)
    rest = REST_SUB.sub(partial(rest_sub, conv), raw_rest)

    return front_us + first + rest + trailing_us
