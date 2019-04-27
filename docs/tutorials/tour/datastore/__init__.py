"""

A customer walks into a store. Do the steps to interact with them:

- Get a correct greeter

- Interact with them

Simple wired application:

- Settings that say what punctuation to use

- Registry

- A bundled Greeter and Customer

- An add-on which defines a FrenchGreeter and FrenchCustomer

- A Datastore which stores/retrieves instances of Customers

"""
from dataclasses import dataclass, field
from typing import List

from wired import ServiceRegistry, ServiceContainer


@dataclass
class Customer:
    name: str


@dataclass
class Datastore:
    customers: List[Customer] = field(default_factory=list)


@dataclass
class Settings:
    punctuation: str


@dataclass
class Greeter:
    punctuation: str
    greeting: str = 'Hello'

    def __call__(self, customer: Customer) -> str:
        return f'{self.greeting} {customer.name} {self.punctuation}'


def setup(registry: ServiceRegistry, settings: Settings):
    """ Initialize the features in the core application  """

    # Make and register the Datastore
    datastore = Datastore()
    registry.register_singleton(datastore, Datastore)

    # **** Default Greeter
    # Make the greeter factory, using punctuation from settings
    punctuation = settings.punctuation

    def default_greeter_factory(container) -> Greeter:
        # Use the dataclass default for greeting
        return Greeter(punctuation=punctuation)

    # Register it as a factory using its class for the "key"
    registry.register_factory(default_greeter_factory, Greeter)

    # During bootstrap, make some Customers
    customer1 = Customer(name='Mary')
    datastore.customers.append(customer1)


def app_bootstrap(settings: Settings) -> ServiceRegistry:
    # Make the registry
    registry = ServiceRegistry()

    # Do setup for the core application features
    setup(registry, settings)

    # Import the add-on and initialize it
    from .custom import setup as addon_setup

    addon_setup(registry, settings)

    return registry


def customer_interaction(
    container: ServiceContainer, customer: Customer
) -> str:
    """ Customer comes in, handle the steps in greeting them """

    # Get a Greeter using the customer as context. Use the Customer when
    # generating the greeting.
    greeter: Greeter = container.get(Greeter, context=customer)
    greeting = greeter(customer)

    return greeting


def sample_interactions(registry: ServiceRegistry) -> List[str]:
    """ Pretend to do a couple of customer interactions """

    greetings = []

    bootstrap_container: ServiceContainer = registry.create_container()
    datastore: Datastore = bootstrap_container.get(Datastore)
    for customer in datastore.customers:
        # Do a sample "interaction" (aka transaction, aka request) for
        # each customer. This is like handling a view for a request.
        interaction_container = registry.create_container()
        greeting = customer_interaction(interaction_container, customer)
        greetings.append(greeting)

    return greetings


def main():
    settings = Settings(punctuation='!!')
    registry = app_bootstrap(settings)
    greetings = sample_interactions(registry)
    assert greetings == ['Hello Mary !!', 'Bonjour Henri !!']


if __name__ == '__main__':
    main()
