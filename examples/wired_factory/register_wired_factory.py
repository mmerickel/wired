"""
A class is a callable that can be the factory supplied to
:func:`wired.ServiceRegistry.register_factory`.
"""

from wired import ServiceContainer, ServiceRegistry


class Greeter:
    def __init__(self, name):
        self.name = name

    @classmethod
    def __wired_factory__(cls, container: ServiceContainer):
        return cls('Marie')


class Greeting:
    def __init__(self, greeter: Greeter):
        self.greeter = greeter

    def greet(self):
        return f'Hello from {self.greeter.name}'

    @classmethod
    def __wired_factory__(cls, container):
        greeter = container.get(Greeter)
        return cls(greeter)


def app():
    # Do this once at startup
    registry = ServiceRegistry()
    registry.register_factory(Greeter, Greeter)
    registry.register_factory(Greeting, Greeting)

    # Do this for every "request" or operation
    container = registry.create_container()
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
