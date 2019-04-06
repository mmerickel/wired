import pytest

from wired import ServiceRegistry


@pytest.fixture
def settings():
    from wired.samples.decoupled import Settings
    settings = Settings(punctuation='!!')
    return settings


@pytest.fixture
def registry(settings):
    from wired.samples.decoupled import setup
    r: ServiceRegistry = setup(settings)
    return r


@pytest.fixture
def default_customer():
    from wired.samples.decoupled import Customer
    return Customer(name='Mary')


@pytest.fixture
def french_customer():
    from wired.samples.decoupled.custom import FrenchCustomer
    return FrenchCustomer(name='Henri')


def test_greet_customer(registry, default_customer):
    from wired.samples.decoupled import greet_customer
    actual = greet_customer(registry, default_customer)
    assert 'Hello Mary !!' == actual


def test_greet_french_customer(registry, french_customer):
    from wired.samples.decoupled import greet_customer
    actual = greet_customer(registry, french_customer)
    assert 'Bonjour Henri !!' == actual
