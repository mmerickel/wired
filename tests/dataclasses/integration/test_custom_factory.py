from dataclasses import dataclass

import pytest
import venusian

from wired import ServiceRegistry
from wired.dataclasses import factory, injected


@pytest.fixture
def registry():
    registry = ServiceRegistry()
    scanner = venusian.Scanner(registry=registry)
    scanner.scan(__import__(__name__))
    return registry


@dataclass
class Url:
    value: str


@dataclass
class Customer:
    name: str


people = dict(
    fred=Customer(name='Fred'),
    alice=Customer(name='Alice')
)


@factory()
@dataclass
class Context:
    @classmethod
    def wired_factory(cls, container):
        url = container.get(Url)
        person = people.get(url.value)
        return person


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

    # Put a URL into the container as the identifier for this
    # "request". The Context can then use it to extract a customer.
    url = Url(value='alice')
    container.register_singleton(url, Url)

    # We now have a pluggable way to get a context, which
    # might be a Customer, a Vendor, an Employee, etc..
    context = container.get(Context)

    # Now get the right greeter for this context
    return container.get(Greeter, context=context)


def test_greeter(greeter: Greeter):
    greeting = greeter()
    assert 'Hello Alice my name is Mary' == greeting
