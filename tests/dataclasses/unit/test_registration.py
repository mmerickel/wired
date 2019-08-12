from dataclasses import dataclass
from typing import Callable, Optional, Any

import pytest
from zope.interface import Interface

from wired import ServiceRegistry
from wired.dataclasses.registration import register_dataclass


@dataclass
class DummyGreeter:
    name: str = 'dummy_greeter'


@dataclass
class DummyCustomer:
    """ Use this as a context in the container """

    name: str = 'dummy_customer'


@pytest.fixture
def dummy_customer():
    return DummyCustomer()


def test_dummy_customer(dummy_customer):
    assert 'dummy_customer' == dummy_customer.name


@dataclass
class DummyRegistry(ServiceRegistry):
    factory: Optional[Callable] = None
    iface_or_type: Optional[Any] = None
    context: Optional[Any] = None

    def register_factory(
        self, factory, iface_or_type=Interface, *, context=None, name=''
    ):
        self.factory = factory
        self.iface_or_type = iface_or_type
        self.context = context


@pytest.fixture
def dummy_registry():
    return DummyRegistry()


@pytest.fixture
def container():
    registry = ServiceRegistry()
    container = registry.create_container()
    return container


def test_basic(dummy_registry: DummyRegistry, container):
    register_dataclass(dummy_registry, DummyGreeter)
    assert DummyGreeter == dummy_registry.iface_or_type
    factory = dummy_registry.factory
    instance: DummyGreeter = factory(container)
    assert 'dummy_greeter' == instance.name


def test_for(dummy_registry: DummyRegistry, container):
    register_dataclass(dummy_registry, DummyGreeter)
    assert DummyGreeter == dummy_registry.iface_or_type
