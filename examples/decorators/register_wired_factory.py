"""
A class is a callable that can be the factory supplied to
:func:`wired.ServiceRegistry.register_factory`.
"""
from wired import ServiceContainer


class Greeter:
    def __init__(self, name):
        self.name = name

    @classmethod
    def __wired_factory__(cls, container: ServiceContainer):
        return cls('Marie')


class Greeting:
    def __init__(self, container: ServiceContainer):
        self.greeter = container.get(Greeter)

    def greet(self):
        return f'Hello from {self.greeter.name}'

    @classmethod
    def __wired_factory__(cls, container: ServiceContainer):
        return cls(container)
