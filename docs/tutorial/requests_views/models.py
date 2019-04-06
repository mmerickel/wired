"""

Models used in the core application.

Putting models in their own file is considered good practice for
code clarity. It also solves the problem of potential circular
imports.

"""

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


@dataclass
class Greeter:
    punctuation: str
    greeting: str = 'Hello'


@dataclass
class View:
    request: Request
    context: Resource
    greeter: Greeter

    def __call__(self) -> str:
        g = self.greeter
        return f'{g.greeting} {self.context.title} {g.punctuation}'
