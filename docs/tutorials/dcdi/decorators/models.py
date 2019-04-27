"""

Models used in the core application.

Putting models in their own file is considered good practice for
code clarity. It also solves the problem of potential circular
imports.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from wired import ServiceContainer

from .decorators import factory, singleton
from .utils import injected


@dataclass(frozen=True)
class Url:
    """ Make it easy to get the currently-processed url """

    value: str


@dataclass(frozen=True)
class Resource:
    """ Base type for the business objects in the system """

    name: str
    title: str

    @staticmethod
    def wired_factory(container: ServiceContainer) -> Resource:
        """ Custom factory that gets a Datastore instance """
        # Presumes that "url" is in the container
        ds: Datastore = container.get(Datastore)
        url: Url = container.get(Url)
        context: Resource = ds.customers.get(url.value)
        return context


@dataclass(frozen=True)
class Customer(Resource):
    """ A Customer resource in the system """

    pass


@singleton()
@dataclass(frozen=True)
class Datastore:
    """ Persistent storage of resources """

    customers: Dict[str, Customer] = field(default_factory=dict)


@dataclass(frozen=True)
class Settings:
    """ Configuration that a site using this app can customize and adjust """

    punctuation: str


@dataclass(frozen=True)
class Request:
    """ Information specific to the currently-processed operation """

    container: ServiceContainer
    url: str = injected(Url, attr='value')


@factory()
@dataclass(frozen=True)
class Greeter:
    """ The person that greets a customer """

    punctuation: str = injected(Settings, attr='punctuation')
    greeting: str = 'Hello'


@factory()
@dataclass(frozen=True)
class View:
    """ Everything needed to process the interaction for current request """

    url: str = injected(Request, attr='url')
    customer_title: str = injected(Resource, attr='title')
    greeting: str = injected(Greeter, attr='greeting')
    punctuation: str = injected(Greeter, attr='punctuation')

    def __call__(self) -> str:
        return (
            f'{self.url}: {self.greeting} {self.customer_title} '
            f'{self.punctuation}'
        )
