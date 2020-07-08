from dataclasses import dataclass
from typing import Protocol


class Component(Protocol):
    name: str


class Greeting(Component, Protocol):
    name: str
    label: str


@dataclass
class FrenchGreeting(Greeting):
    label: str = 'Bonjour'


if __name__ == '__main__':
    fh = FrenchGreeting()
    print(fh)
