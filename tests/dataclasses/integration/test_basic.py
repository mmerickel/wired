from dataclasses import dataclass

import pytest
from wired import ServiceRegistry, ServiceContainer
from wired.dataclasses import Context
from wired.dataclasses.registration import register_dataclass


@dataclass
class Greeter:
    name: str = 'greeter'


@dataclass
class Customer(Context):
    name: str = 'customer'

    @classmethod
    def wired_factory(cls, container: ServiceContainer):
        mary = cls(name='mary')
        return mary


@pytest.fixture
def registry():
    return ServiceRegistry()


@pytest.fixture
def container(registry):
    return registry.create_container()


def test_simple(registry, container):
    register_dataclass(registry, Greeter)
    instance: Greeter = container.get(Greeter)
    assert 'greeter' == instance.name


def test_context(registry, container):
    register_dataclass(registry, Customer, for_=Context)
    instance: Greeter = container.get(Context)
    assert 'mary' == instance.name
