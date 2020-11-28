"""
Use :func:`wired.ServiceRegistry.register_factory` with
a class as the factory callable, rather than a separate
function.
"""


def test_greeter(container, registry):
    from examples.decorators.register_factory_basic import (
        greeter_factory,
        Greeter,
        greeting_factory,
        Greeting,
    )

    registry.register_factory(greeter_factory, Greeter)
    registry.register_factory(greeting_factory, Greeting)
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
