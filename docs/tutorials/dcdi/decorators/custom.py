"""

A custom add-on to our app which adds FrenchCustomer and
French Greeter.

"""
from dataclasses import dataclass

from wired import ServiceRegistry
from .decorators import factory
from .models import (
    Customer,
    Greeter,
    Request,
    Resource,
    Datastore,
    Settings,
    View,
)
from .utils import injected


@dataclass(frozen=True)
class FrenchCustomer(Customer):
    """ A custom kind of Customer """

    pass


@factory(for_=Greeter, context=FrenchCustomer)
@dataclass(frozen=True)
class FrenchGreeter(Greeter):
    """ A customer kind of Greeter """

    greeting: str = 'Bonjour'


@factory(for_=View, context=FrenchCustomer)
@dataclass(frozen=True)
class FrenchView:
    settings: Settings
    url: str = injected(Request, attr='url')
    customer_title: str = injected(Resource, attr='title')
    greeting: str = injected(Greeter, attr='greeting')

    def __call__(self) -> str:
        return (
            f'{self.url} and FrenchView: {self.greeting} '
            f'{self.customer_title} {self.settings.punctuation}'
        )


def setup(registry: ServiceRegistry, datastore: Datastore):
    # Grab the Datastore and add a FrenchCustomer
    henri = FrenchCustomer(name='henri', title='Henri')
    datastore.customers['henri'] = henri
