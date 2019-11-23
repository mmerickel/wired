from dataclasses import dataclass
import pytest

from wired import ServiceContainer, ServiceRegistry
from wired.dataclasses.registration import register_dataclass


@dataclass
class DummyGreeter:
    name: str = 'dummy_greeter'


@dataclass
class DummyCustomer:
    """ Use this as a context in the container """

    name: str = 'dummy_customer'


@pytest.fixture
def registry():
    return ServiceRegistry()


@pytest.fixture
def container(registry):
    return registry.create_container()


def test_basic(registry: ServiceRegistry, container: ServiceContainer):
    register_dataclass(registry, DummyGreeter)
    register_dataclass(registry, DummyCustomer)
    greeter: DummyGreeter = container.get(DummyGreeter)
    customer: DummyCustomer = container.get(DummyCustomer)
    assert 'dummy_greeter' == greeter.name
    assert 'dummy_customer' == customer.name
