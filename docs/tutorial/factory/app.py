"""

A customer walks into a store. Do the steps to interact with them:

- Get *a* (not *the*) greeter

- Interact with them

Simple wired application:

- Registry

- Factory to get a Greeter that says hello

"""
from dataclasses import dataclass

from wired import ServiceRegistry


@dataclass
class Greeter:
    greeting: str

    def __call__(self) -> str:
        return f'{self.greeting} !!'


def setup() -> ServiceRegistry:
    # Make the registry
    registry = ServiceRegistry()

    # Make the greeter factory
    def greeter_factory(container) -> Greeter:
        return Greeter(greeting='Hello')

    # Register it as a factory using its class for the "key"
    registry.register_factory(greeter_factory, Greeter)

    return registry


def greet_a_customer(registry: ServiceRegistry) -> str:
    # A customer comes in, handle the steps in the greeting
    # as a container.
    container = registry.create_container()

    # First step in the interaction: get a greeter
    the_greeter: Greeter = container.get(Greeter)

    # Now do the steps in the interaction
    greeting = the_greeter()
    return greeting


def main():
    registry = setup()
    greeting = greet_a_customer(registry)
    assert greeting == 'Hello !!'
