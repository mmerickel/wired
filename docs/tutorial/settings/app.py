"""

A customer walks into a store. Do the steps to interact with them:

- See what kind of customer it is

- Get a greeter based on the kind of customer

- Interact with them

Simple wired application:

- Settings that say what punctuation to use

- Registry

- Factory that says hello

"""
from dataclasses import dataclass

from wired import ServiceRegistry


@dataclass
class Settings:
    punctuation: str


@dataclass
class Greeter:
    greeting: str
    punctuation: str

    def __call__(self) -> str:
        return f'{self.greeting} {self.punctuation}'


def setup(settings: Settings) -> ServiceRegistry:
    # Make the registry
    registry = ServiceRegistry()

    # Make the greeter factory, using punctuation from settings
    punctuation = settings.punctuation

    def greeter_factory(container) -> Greeter:
        return Greeter(greeting='Hello', punctuation=punctuation)

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
    settings = Settings(punctuation='!!')
    registry = setup(settings)
    greeting = greet_a_customer(registry)
    assert greeting == 'Hello !!'
