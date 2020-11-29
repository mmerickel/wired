"""
Simplest example for ``@service_factory`` decorator: a basic class.
"""
from venusian import Scanner

from wired import service_factory, ServiceRegistry
from .. import decorators


@service_factory()
class Greeting:
    def __init__(self, container):
        self.greeter = container.get(Greeter)

    def greet(self):
        return f'Hello from {self.greeter.name}'


class Greeter:
    def __init__(self, name):
        self.name = name


def greeter_factory(container):
    return Greeter('Marie')


def app():
    # Do this once at startup
    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    # Point the scanner at a package/module and scan
    scanner.scan(decorators.basic_class)

    registry.register_factory(greeter_factory, Greeter)
    # No longer need this line
    # registry.register_factory(Greeting, Greeting)

    # Do this for every "request" or operation
    container = registry.create_container()
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
