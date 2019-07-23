# models.py
from dataclasses import dataclass

from wired.dataclasses import factory

@factory

@factory()
@dataclass
class Greeter:
    """ A basic greeter """
    name: str = 'Mary'

    def __call__(self):
        return f'Hello my name is {self.name}'
