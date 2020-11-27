"""
Starting-point example that uses no decorator nor
``wired_factory`` support but the ``Greeting`` class
 serves as its factory.

"""
import pytest

from examples.decorators import no_decorator


@pytest.fixture
def scannable():
    return no_decorator


def test_greeter(container, registry):
    from examples.decorators.no_decorator import (
        greeter_factory,
        Greeter,
        greeting_factory,
        Greeting,
    )
    registry.register_factory(greeter_factory, Greeter)
    registry.register_factory(greeting_factory, Greeting)
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
