"""
Decorators for both plus usage of the ``__wired_factory__ protocol.
"""
from venusian import Scanner

from wired import service_factory, ServiceRegistry
from .. import decorators


@service_factory()
class Greeter:
    def __init__(self, name):
        self.name = name

    @classmethod
    def __wired_factory__(cls, container):
        return cls('Marie')


@service_factory()
class Greeting:
    greeter: Greeter

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
    scanner = Scanner(registry=registry)
    # Point the scanner at a package/module and scan
    scanner.scan(decorators.decorator_with_wired_factory)

    # Do this for every "request" or operation
    container = registry.create_container()
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
