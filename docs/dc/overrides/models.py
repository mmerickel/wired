# models.py
from dataclasses import dataclass

from wired.dataclasses import factory


@factory()
@dataclass
class Settings:
    """ Store some configuration settings for the app """

    punctuation: str = '.'


@dataclass
class Customer:
    """ A basic customer """

    name: str = 'Larry'


@dataclass
class FrenchCustomer:
    """ A certain kind of customer """

    name: str = 'Anne'


@factory()
@dataclass
class Greeter:
    """ A basic greeter """

    settings: Settings
    name: str = 'Mary'

    def __call__(self, customer):
        punctuation = self.settings.punctuation
        return f'Hello {customer} my name is {self.name}{punctuation}'


@factory(for_=Greeter, context=FrenchCustomer)
@dataclass
class FrenchGreeter:
    """ A greeter to use when the customer (context) is French """

    settings: Settings
    name: str = 'Henri'

    def __call__(self, customer):
        punctuation = self.settings.punctuation
        return f'Salut {customer} je m\'apelle {self.name}{punctuation}'
