"""

A custom add-on to our app which adds FrenchCustomer and
French Greeter.

"""
from dataclasses import dataclass

from wired import ServiceRegistry
from . import Customer, Greeter, Settings


@dataclass
class FrenchCustomer(Customer):
    pass


@dataclass
class FrenchGreeter(Greeter):
    greeting: str = 'Bonjour'


def setup(registry: ServiceRegistry, settings: Settings):
    # The French greeter, using context of FrenchCustomer
    punctuation = settings.punctuation

    def french_greeter_factory(container) -> Greeter:
        # Use the dataclass default for greeting
        return FrenchGreeter(punctuation=punctuation)

    # Register it as a factory using its class for the "key", but
    # this time register with a "context"
    registry.register_factory(
        french_greeter_factory, Greeter, context=FrenchCustomer
    )
