import pytest
from venusian import Scanner

from wired import ServiceRegistry


@pytest.fixture
def scannable():
    """ Each test file needs to implement this """
    raise NotImplementedError()


@pytest.fixture
def registry():
    return ServiceRegistry()


@pytest.fixture
def container(registry, scannable):
    s = Scanner(registry=registry)
    s.scan(scannable)
    c = registry.create_container()
    return c
