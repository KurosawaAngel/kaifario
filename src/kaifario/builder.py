from typing import Self

from kaifario.configuration import Configuration
from kaifario.protocols.provider import ConfigurationProvider


class ConfigurationBuilder:
    _providers: list[ConfigurationProvider]

    def __init__(self) -> None:
        self._providers = []

    def add_provider(self, provider: ConfigurationProvider) -> Self:
        self._providers.append(provider)
        return self

    def add_providers(self, *providers: ConfigurationProvider) -> Self:
        self._providers.extend(providers)
        return self

    def build(self) -> Configuration:
        data = {}
        for provider in self._providers:
            data.update(provider.load())
        return Configuration(data)
