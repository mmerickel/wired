import pytest

from examples.decorators import basic_class


@pytest.fixture
def scannable():
    return basic_class


def test_greeter(container, registry):
    from examples.decorators.basic_class import (
        greeter_factory,
        Greeter,
        Greeting,
    )

    registry.register_factory(greeter_factory, Greeter)
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
