from dataclasses import dataclass, field

import pytest
import venusian

from wired import ServiceRegistry, ServiceContainer
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
    container: ServiceContainer
    punctuation: str = field(init=False)
    name: str = 'Mary'

    def __post_init__(self):
        p: Punctuation = self.container.get(Punctuation)
        self.punctuation = p.value

    def __call__(self, customer):
        return f'Hello {customer} my name is {self.name} {self.punctuation}'


@pytest.fixture
def greeter(registry) -> Greeter:
    container = registry.create_container()
    return container.get(Greeter)


def test_greeter(greeter: Greeter):
    greeting = greeter('Larry')
    assert 'Hello Larry my name is Mary !!' == greeting
