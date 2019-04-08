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


@dataclass
class Url:
    value: str


@dataclass
class Resource:
    name: str
    title: str

    @staticmethod
    def factory(container: ServiceContainer) -> Resource:
        # Presumes that "url" is in the container
        ds: Datastore = container.get(Datastore)
        url: str = container.get(Url)
        context: Resource = ds.customers.get(url)
        return context


@dataclass
class Customer(Resource):
    pass


@dataclass
class Datastore:
    customers: Dict[str, Customer] = field(default_factory=dict)


@dataclass
class Settings:
    punctuation: str


@dataclass
class Request:
    url: str
    container: ServiceContainer

    @staticmethod
    def factory(container: ServiceContainer) -> Request:
        url: str = container.get(Url)
        request = Request(url=url, container=container)
        return request


@dataclass
class Greeter:
    settings: Settings
    greeting: str = 'Hello'

    @property
    def punctuation(self):
        return self.settings.punctuation


@dataclass
class View:
    request: Request
    context: Resource
    greeter: Greeter

    @staticmethod
    def factory(container: ServiceContainer) -> View:
        request: Request = container.get(Request)
        context: Resource = container.get(Resource)
        greeter: Greeter = container.get(Greeter, context=context)
        view = View(request=request, context=context, greeter=greeter)
        return view

    def __call__(self) -> str:
        g = self.greeter
        return f'{g.greeting} {self.context.title} {g.punctuation}'
