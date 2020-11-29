from wired import ServiceRegistry, ServiceContainer


class Greeter:
    def __init__(self, name):
        self.name = name


def greeter_factory(container):
    return Greeter('Marie')


class Greeting:
    def __init__(self, greeter: Greeter):
        self.greeter = greeter

    def greet(self):
        return f'Hello from {self.greeter.name}'


def greeting_factory(container: ServiceContainer):
    greeter = container.get(Greeter)
    return Greeting(greeter)


def app():
    # Do this once at startup
    registry = ServiceRegistry()
    registry.register_factory(greeter_factory, Greeter)
    registry.register_factory(greeting_factory, Greeting)

    # Do this for every "request" or operation
    container = registry.create_container()
    greeting: Greeting = container.get(Greeting)
    assert 'Hello from Marie' == greeting.greet()
