import sys

import pytest

from wired import ServiceRegistry


@pytest.fixture
def registry():
    from simple.app import setup
    r: ServiceRegistry = setup()
    return r


@pytest.mark.skipif(sys.version_info < (3, 7),
                    reason="requires python3.3")
def test_greet_a_customer(registry):
    from simple.app import greet_a_customer
    actual = greet_a_customer(registry)
    assert 'Hello !!' == actual
