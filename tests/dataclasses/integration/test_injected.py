from dataclasses import dataclass

import pytest
import venusian

from wired import ServiceRegistry
from wired.dataclasses import factory


@factory()
@dataclass
class Customer:
    name: str = 'Fred'


@factory()
@dataclass
class FrenchCustomer:
    name: str = 'Anne'
    age: int = '40'


@pytest.fixture
def registry():
    registry = ServiceRegistry()
    scanner = venusian.Scanner(registry=registry)
    scanner.scan(__import__(__name__))
    return registry


@factory()
@dataclass
class Greeter:
    customer: Customer
    name: str = 'Mary'

    def __call__(self):
        msg = f'Hello {self.customer.name} my name is {self.name}'
        return msg


@factory(for_=Greeter, context=FrenchCustomer)
@dataclass
class FrenchGreeter:
    customer: FrenchCustomer
    name: str = 'Henri'

    def __call__(self):
        msg = f'Salut {self.customer.name} je m\'apelle {self.name}'
        return msg


@pytest.fixture
def greeter(registry) -> Greeter:
    container = registry.create_container()
    context = Customer()
    return container.get(Greeter, context=context)


@pytest.fixture
def french_greeter(registry) -> Greeter:
    container = registry.create_container()
    context = FrenchCustomer()
    return container.get(Greeter, context=context)


def test_greeter(greeter: Greeter):
    greeting = greeter()
    assert 'Hello Fred my name is Mary' == greeting


def test_french_greeter(french_greeter: FrenchGreeter):
    greeting = french_greeter()
    assert 'Salut Anne je m\'apelle Henri' == greeting
