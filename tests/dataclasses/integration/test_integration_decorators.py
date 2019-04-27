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
class Greeter:
    name: str = 'Mary'

    def __call__(self, customer):
        return f'Hello {customer} my name is {self.name}'


@pytest.fixture
def greeter(registry) -> Greeter:
    container = registry.create_container()
    return container.get(Greeter)


def test_greeter(greeter: Greeter):
    greeting = greeter('Larry')
    assert 'Hello Larry my name is Mary' == greeting
