from dataclasses import dataclass

import pytest
import venusian

from wired import ServiceRegistry
from wired.dataclasses import factory, injected


class Context:
    """ Just a marker """


@dataclass
class Customer:
    name: str = 'Fred'


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
    customer: Customer = injected(Context)
    name: str = 'Mary'

    def __call__(self):
        msg = f'Hello {self.customer.name} my name is {self.name}'
        return msg


@factory(for_=Greeter, context=FrenchCustomer)
@dataclass
class FrenchGreeter:
    customer: FrenchCustomer = injected(Context)
    name: str = 'Henri'

    def __call__(self):
        msg = f'Salut {self.customer.name} je m\'apelle {self.name}'
        return msg


@pytest.fixture
def greeter(registry) -> Greeter:
    container = registry.create_container()
    customer = Customer()
    # Register this in the container as the "context"
    container.register_singleton(customer, Context)
    return container.get(Greeter, context=customer)


@pytest.fixture
def french_greeter(registry) -> Greeter:
    container = registry.create_container()
    french_customer = FrenchCustomer()
    # Register this in the container as the "context"
    container.register_singleton(french_customer, Context)
    return container.get(Greeter, context=french_customer)


def test_greeter(greeter: Greeter):
    greeting = greeter()
    assert 'Hello Fred my name is Mary' == greeting


def test_french_greeter(french_greeter: FrenchGreeter):
    greeting = french_greeter()
    assert 'Salut Anne je m\'apelle Henri' == greeting
