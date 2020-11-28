"""
Use :func:`wired.ServiceRegistry.register_factory` with
a class that has the ``__wired_factory__`` class method
but no decorator..
"""


def test_greeter(container, registry):
    from examples.decorators.register_wired_factory import (
        Greeter,
        Greeting,
    )

    registry.register_factory(Greeter, Greeter)
    registry.register_factory(Greeting, Greeting)
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
