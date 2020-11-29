"""
Decorators for both plus usage of the ``__wired_factory__ protocol.
"""
from venusian import Scanner

from wired import service_factory, ServiceRegistry
from .. import decorators


class Customer:
    def __init__(self):
        self.name = 'Jill'


class FrenchCustomer(Customer):
    def __init__(self):
        super().__init__()
        self.name = 'Juliette'


@service_factory(context=Customer)
class Greeter:
    def __init__(self, name):
        self.name = name

    @classmethod
    def __wired_factory__(cls, container):
        return cls('Susan')


@service_factory(for_=Greeter, context=FrenchCustomer)
class FrenchGreeter:
    """ Serves as Greeter when container.context is FrenchCustomer """
    def __init__(self, name):
        self.name = name

    @classmethod
    def __wired_factory__(cls, container):
        return cls('Marie')


@service_factory(context=Customer)
class Greeting:
    greeter: Greeter

    def __init__(self, greeter: Greeter, customer):
        self.greeter = greeter
        self.customer = customer

    def greet(self):
        return f'Hello from {self.greeter.name} to {self.customer.name}'

    @classmethod
    def __wired_factory__(cls, container):
        greeter = container.get(Greeter)
        customer = container.context
        return cls(greeter, customer)


def app():
    # Do this once at startup
    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    # Point the scanner at a package/module and scan
    scanner.scan(decorators.decorator_args)

    # First request, for a regular Customer
    customer1 = Customer()
    container1 = registry.create_container(context=customer1)
    greeting1: Greeting = container1.get(Greeting)
    assert 'Hello from Susan to Jill' == greeting1.greet()

    # Second request, for a FrenchCustomer
    customer2 = FrenchCustomer()
    container2 = registry.create_container(context=customer2)
    greeting2: Greeting = container2.get(Greeting)
    assert 'Hello from Marie to Juliette' == greeting2.greet()
