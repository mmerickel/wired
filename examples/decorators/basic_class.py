"""
Simplest example for ``@factory`` decorator: a basic class.
"""
from wired import ServiceContainer
from wired import factory


class Greeter:
    def __init__(self, name):
        self.name = name


@factory()
class Greeting:
    def __init__(self, container: ServiceContainer):
        self.greeter = container.get(Greeter)

    def greet(self):
        return f'Hello from {self.greeter.name}'


def greeter_factory(container):
    return Greeter('Marie')
