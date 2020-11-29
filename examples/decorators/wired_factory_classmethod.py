"""
Simple usage of a ``_wired_factory__`` classmethod.
"""
from wired import ServiceContainer
from wired import service_factory


@service_factory()
class Greeter:
    def __init__(self, name):
        self.name = name

    @classmethod
    def __wired_factory__(cls, container: ServiceContainer):
        return Greeter('Marie')


@service_factory()
class Greeting:
    def __init__(self, container: ServiceContainer):
        self.greeter = container.get(Greeter)

    def greet(self):
        return f'Hello from {self.greeter.name}'
