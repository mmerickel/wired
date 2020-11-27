import pytest

from wired import ServiceRegistry


@pytest.fixture
def registry():
    from tutorial.simple.app import setup

    r: ServiceRegistry = setup()
    return r


def test_greet_a_customer(registry):
    from tutorial.simple.app import greet_a_customer

    actual = greet_a_customer(registry)
    assert 'Hello !!' == actual


def test_main():
    from tutorial.simple.app import main

    assert None is main()
