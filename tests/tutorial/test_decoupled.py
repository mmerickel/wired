import sys

import pytest

from wired import ServiceRegistry


@pytest.fixture
def settings():
    from decoupled import Settings
    settings = Settings(punctuation='!!')
    return settings


@pytest.fixture
def registry(settings):
    from decoupled import setup
    r: ServiceRegistry = setup(settings)
    return r


@pytest.fixture
def default_customer():
    from decoupled import Customer
    return Customer(name='Mary')


@pytest.fixture
def french_customer():
    from decoupled.custom import FrenchCustomer
    return FrenchCustomer(name='Henri')

@pytest.mark.skipif(sys.version_info < (3, 7),
                    reason="requires python3.3")
def test_greet_customer(registry, default_customer):
    from decoupled import greet_customer
    actual = greet_customer(registry, default_customer)
    assert 'Hello Mary !!' == actual


@pytest.mark.skipif(sys.version_info < (3, 7),
                    reason="requires python3.3")
def test_greet_french_customer(registry, french_customer):
    from decoupled import greet_customer
    actual = greet_customer(registry, french_customer)
    assert 'Bonjour Henri !!' == actual
