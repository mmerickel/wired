from dataclasses import dataclass

import pytest
import venusian

from wired import ServiceRegistry
from wired.dataclasses import factory


@dataclass
class FrenchCustomer:
    name: str = 'Anne'


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

    def __call__(self):
        return f'Hello my name is {self.name}'


@factory(for_=Greeter, context=FrenchCustomer)
@dataclass
class FrenchGreeter:
    name: str = 'Henri'

    def __call__(self):
        return f'Salut je m\'apelle {self.name}'


@pytest.fixture
def greeter(registry) -> Greeter:
    container = registry.create_container()
    return container.get(Greeter)


@pytest.fixture
def french_greeter(registry) -> Greeter:
    container = registry.create_container()
    context = FrenchCustomer()
    return container.get(Greeter, context=context)


def test_greeter(greeter: Greeter):
    greeting = greeter()
    assert 'Hello my name is Mary' == greeting


def test_french_greeter(french_greeter: FrenchGreeter):
    greeting = french_greeter()
    assert 'Salut je m\'apelle Henri' == greeting
