import sys

import pytest

from wired import ServiceRegistry

if sys.version_info < (3, 7):  # pragma: no cover
    collect_ignore_glob = ['*.py']
else:
    from venusian import Scanner


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
