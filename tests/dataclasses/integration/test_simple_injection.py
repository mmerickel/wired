from dataclasses import dataclass

import pytest
import venusian

from wired import ServiceRegistry
from wired.dataclasses import factory


@pytest.fixture
def registry():
    registry = ServiceRegistry()
    scanner = venusian.Scanner(registry=registry)
    scanner.scan(__import__(__name__))
    return registry


@factory()
@dataclass
class Punctuation:
    value: str = '!!'


@factory()
@dataclass
class Greeter:
    punctuation: Punctuation
    name: str = 'Mary'

    def __call__(self, customer):
        return f'Hello {customer} my name is {self.name} {self.punctuation.value}'


@pytest.fixture
def greeter(registry) -> Greeter:
    container = registry.create_container()
    return container.get(Greeter)


def test_greeter(greeter):
    greeting = greeter('Larry')
    assert 'Hello Larry my name is Mary !!' == greeting

