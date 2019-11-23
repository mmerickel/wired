"""

Models used in the core application.

Putting models in their own file is considered good practice for
code clarity. It also solves the problem of potential circular
imports.

"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Customer:
    name: str


@dataclass
class Datastore:
    customers: List[Customer] = field(default_factory=list)


@dataclass
class Settings:
    punctuation: str


@dataclass
class Greeter:
    punctuation: str
    greeting: str = 'Hello'

    def __call__(self, customer: Customer) -> str:
        return f'{self.greeting} {customer.name} {self.punctuation}'
