from wired import ServiceContainer


class Greeter:
    def __init__(self, name):
        self.name = name


class Greeting:
    def __init__(self, container: ServiceContainer):
        self.greeter = container.get(Greeter)

    def greet(self):
        return f'Hello from {self.greeter.name}'


def greeter_factory(container):
    return Greeter('Marie')
