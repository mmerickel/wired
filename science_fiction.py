from dataclasses import dataclass
from typing import Protocol


class Component(Protocol):
    name: str


class Greeting(Component, Protocol):
    label2: str


# @dataclass
class FrenchGreeting(Greeting):
    name: str = 'Marie'
    label: str = 'Bonjour'


if __name__ == '__main__':
    fh = FrenchGreeting()
    print(fh)
