"""

A custom add-on to our app which adds FrenchCustomer and
French Greeter.

"""
from dataclasses import dataclass

from wired import ServiceRegistry
from .models import Customer, Greeter, Datastore
from .utils import register_dataclass


@dataclass(frozen=True)
class FrenchCustomer(Customer):
    """ A custom kind of Customer """

    pass


@dataclass(frozen=True)
class FrenchGreeter(Greeter):
    """ A customer kind of Greeter """

    greeting: str = 'Bonjour'


def setup(registry: ServiceRegistry, datastore: Datastore):
    register_dataclass(
        registry, FrenchGreeter, Greeter, context=FrenchCustomer
    )

    # Add a FrenchCustomer to the datastore
    henri = FrenchCustomer(name='henri', title='Henri')
    datastore.customers['henri'] = henri
