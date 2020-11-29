"""

A customer walks into a store. Do the steps to interact with them:

- Get a correct greeter

- Interact with them

Simple wired application:

- Settings that say what punctuation to use

- Registry

- A bundled Greeter and Customer

- An add-on which defines a FrenchGreeter and FrenchCustomer

"""
from dataclasses import dataclass

from wired import ServiceRegistry


@dataclass
class Customer:
    name: str


@dataclass
class Settings:
    punctuation: str


@dataclass
class Greeter:
    punctuation: str
    greeting: str = 'Hello'

    def __call__(self, customer: Customer) -> str:
        return f'{self.greeting} {customer.name} {self.punctuation}'


def setup(settings: Settings) -> ServiceRegistry:
    # Make the registry
    registry = ServiceRegistry()

    # Make the greeter factory, using punctuation from settings
    punctuation = settings.punctuation

    # First the default greeter, no context
    def default_greeter_factory(container) -> Greeter:
        # Use the dataclass default for greeting
        return Greeter(punctuation=punctuation)

    # Register it as a factory using its class for the "key"
    registry.register_factory(default_greeter_factory, Greeter)

    # Import the add-on and initialize it
    from .custom import setup

    setup(registry, settings)

    return registry


def greet_customer(registry: ServiceRegistry, customer: Customer) -> str:
    # A customer comes in, handle the steps in the greeting
    # as a container.
    container = registry.create_container()

    # Get a Greeter using the customer as context. Use the Customer when
    # generating the greeting.
    greeter: Greeter = container.get(Greeter, context=customer)
    greeting = greeter(customer)

    return greeting


def main():
    settings = Settings(punctuation='!!')
    registry = setup(settings)

    # *** Default Customer
    # Make a Customer, pass into the "greet_customer" interaction,
    # then test the result.
    customer = Customer(name='Mary')
    assert 'Hello Mary !!' == greet_customer(registry, customer)

    # *** French Customer
    # Make a FrenchCustomer, pass into the "greet_customer" interaction,
    # then test the result.
    from .custom import FrenchCustomer

    french_customer = FrenchCustomer(name='Henri')
    assert 'Bonjour Henri !!' == greet_customer(registry, french_customer)
