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
    value: str


@dataclass(frozen=True)
class Resource:
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
    pass


@singleton()
@dataclass(frozen=True)
class Datastore:
    customers: Dict[str, Customer] = field(default_factory=dict)


@dataclass(frozen=True)
class Settings:
    punctuation: str


@dataclass(frozen=True)
class Request:
    container: ServiceContainer
    url: str = injected(Url, attr='value')


@factory()
@dataclass(frozen=True)
class Greeter:
    punctuation: str = injected(Settings, attr='punctuation')
    greeting: str = 'Hello'


@factory()
@dataclass(frozen=True)
class View:
    url: str = injected(Request, attr='url')
    customer_title: str = injected(Resource, attr='title')
    greeting: str = injected(Greeter, attr='greeting')
    punctuation: str = injected(Greeter, attr='punctuation')

    def __call__(self) -> str:
        return f'{self.url}: {self.greeting} {self.customer_title} {self.punctuation}'
