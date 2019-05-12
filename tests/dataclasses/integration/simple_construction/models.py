# models.py
from dataclasses import dataclass


@dataclass
class Greeter:
    name: str = 'Mary'

    def __call__(self, customer):
        return f'Hello {customer} my name is {self.name}'
