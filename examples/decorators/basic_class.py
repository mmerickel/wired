"""
Simplest example for ``@service_factory`` decorator: a basic class.
"""
from wired import service_factory


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
