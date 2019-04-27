"""

A custom add-on to our app which adds FrenchCustomer and
French Greeter.

"""
from dataclasses import dataclass

from wired import ServiceRegistry
from .models import Customer, Greeter, Datastore
from .utils import register_dataclass


@dataclass
class FrenchCustomer(Customer):
    """ A custom kind of Customer """

    pass


@dataclass
class FrenchGreeter(Greeter):
    """ A customer kind of Greeter """

    greeting: str = 'Bonjour'


def setup(registry: ServiceRegistry):
    register_dataclass(
        registry,
        FrenchGreeter, Greeter,
        context=FrenchCustomer
    )

    # Grab the Datastore and add a FrenchCustomer
    container = registry.create_container()
    datastore: Datastore = container.get(Datastore)
    henri = FrenchCustomer(name='henri', title='Henri')
    datastore.customers['henri'] = henri
