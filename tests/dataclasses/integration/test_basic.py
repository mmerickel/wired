from dataclasses import dataclass

import pytest

from wired import ServiceRegistry
from wired.dataclasses.registration import register_dataclass


@dataclass
class Greeter:
    name: str = 'greeter'


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
