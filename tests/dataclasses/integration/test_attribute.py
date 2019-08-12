from dataclasses import dataclass

import pytest
import venusian

from wired import ServiceRegistry
from wired.dataclasses import factory, injected


class Context:
    """ Just a marker """

    pass


@dataclass
class Customer:
    name: str = 'Fred'


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


@pytest.fixture
def greeter(registry) -> Greeter:
    container = registry.create_container()
    customer = Customer()
    # Register this in the container as the "context"
    container.register_singleton(customer, Context)
    return container.get(Greeter, context=customer)


def test_greeter(greeter: Greeter):
    greeting = greeter()
    assert 'Hello Fred my name is Mary' == greeting
