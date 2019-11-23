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

- Request and View factories to assemble the full processing chain

"""
from typing import List

from wired import ServiceRegistry
from .models import (
    Customer,
    Datastore,
    Greeter,
    Resource,
    Request,
    Settings,
    View,
)
from .utils import process_request, register_dataclass


def app_bootstrap(settings: Settings) -> ServiceRegistry:
    # Make the registry
    registry = ServiceRegistry()

    # Store the settings in the registry so things later can
    # get to them.
    registry.register_singleton(settings, Settings)

    # Make and register the Datastore singleton
    datastore = Datastore()
    registry.register_singleton(datastore, Datastore)

    # Do setup for the core application features
    setup(registry, datastore)

    # Import the add-on and initialize it
    from .custom import setup as addon_setup

    addon_setup(registry, datastore)

    return registry


def setup(registry: ServiceRegistry, datastore: Datastore):
    """ Initialize the features in the core application  """

    for dc in (Resource, Request, Greeter, View):
        register_dataclass(registry, dc)

    # During bootstrap, make some Customers
    mary = Customer(name='mary', title='Mary')
    datastore.customers['mary'] = mary


def sample_interactions(registry: ServiceRegistry) -> List[str]:
    """ Pretend to do a couple of customer interactions """

    return [process_request(registry, url) for url in ('mary', 'henri')]


def main():
    settings = Settings(punctuation='!!')
    registry = app_bootstrap(settings)
    greetings = sample_interactions(registry)
    assert greetings == ['Hello Mary !!', 'Bonjour Henri !!']


if __name__ == '__main__':
    main()
