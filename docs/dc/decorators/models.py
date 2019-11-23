# models.py
from dataclasses import dataclass

from wired.dataclasses import factory


@factory()
@dataclass
class Greeter:
    name: str = 'Mary'

    def __call__(self, customer):
        return f'Hello {customer} my name is {self.name}'
