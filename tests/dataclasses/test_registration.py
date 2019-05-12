from dataclasses import dataclass
from typing import Callable, Optional, Any

import pytest
from wired import ServiceRegistry, ServiceContainer
from wired.dataclasses import Context
from wired.dataclasses.registration import register_dataclass
from zope.interface import Interface


@dataclass
class DummyGreeter:
    name: str = 'dummy_greeter'


@dataclass
class DummyWiredGreeter:
    name: str = 'dummy_greeter'

    @classmethod
    def wired_factory(cls, container: ServiceContainer):
        return DummyGreeter(name='dummy_wired_greeter')


@dataclass
class DummyContext(Context):
    pass


@dataclass
class DummyRegistry(ServiceRegistry):
    factory: Optional[Callable] = None
    iface_or_type: Optional[Any] = None
    context: Optional[Any] = None

    def register_factory(
            self, factory, iface_or_type=Interface, *,
            context=None, name=''):
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


@pytest.fixture
def dummy_context():
    return DummyContext()


def test_basic(dummy_registry: DummyRegistry, container, dummy_context):
    register_dataclass(dummy_registry, DummyGreeter, context=dummy_context)
    assert DummyGreeter == dummy_registry.iface_or_type
    factory = dummy_registry.factory
    instance: DummyGreeter = factory(container)
    assert 'dummy_greeter' == instance.name


def test_wired_factory(dummy_registry: DummyRegistry,
                       container, dummy_context):
    register_dataclass(dummy_registry, DummyWiredGreeter,
                       context=dummy_context)
    assert DummyWiredGreeter == dummy_registry.iface_or_type
    factory = dummy_registry.factory
    instance: DummyWiredGreeter = factory(container)
    assert 'dummy_wired_greeter' == instance.name


def test_for(dummy_registry: DummyRegistry, container, dummy_context):
    register_dataclass(
        dummy_registry,
        DummyWiredGreeter,
        for_=DummyGreeter
    )
    assert DummyGreeter == dummy_registry.iface_or_type