from wired import ServiceContainer, ServiceRegistry


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


def app():
    # Do this once at startup
    registry = ServiceRegistry()
    registry.register_factory(greeter_factory, Greeter)
    registry.register_factory(Greeting, Greeting)

    # Do this for every "request" or operation
    container = registry.create_container()
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
