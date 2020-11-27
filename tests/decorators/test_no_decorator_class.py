"""
Starting-point example that uses no decorator nor
``wired_factory`` support.

"""
import pytest

from examples.decorators import no_decorator_class


@pytest.fixture
def scannable():
    return no_decorator_class


def test_greeter(container, registry):
    from examples.decorators.no_decorator_class import (
        greeter_factory,
        Greeter,
        Greeting,
    )
    registry.register_factory(greeter_factory, Greeter)
    registry.register_factory(Greeting, Greeting)
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
