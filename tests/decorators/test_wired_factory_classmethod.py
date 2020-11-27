import pytest

from examples.decorators import wired_factory_classmethod


@pytest.fixture
def scannable():
    return wired_factory_classmethod


def test_greeter(container, registry):
    from examples.decorators.wired_factory_classmethod import Greeting
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
