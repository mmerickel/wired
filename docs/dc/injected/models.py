# models.py
from dataclasses import dataclass

from wired.dataclasses import factory, injected, Context


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


@factory(context=Customer)
@dataclass
class Greeter:
    """ A basic greeter """

    settings: Settings
    customer: Customer = injected(Context)
    name: str = 'Mary'

    def __call__(self):
        punctuation = self.settings.punctuation
        m = f'my name is {self.name}{punctuation}'
        return f'Hello {self.customer.name} {m}'


@factory(for_=Greeter, context=FrenchCustomer)
@dataclass
class FrenchGreeter:
    """ A greeter to use when the customer (context) is French """

    settings: Settings
    customer: FrenchCustomer = injected(Context)
    name: str = 'Henri'

    def __call__(self):
        punctuation = self.settings.punctuation
        m = f'je m\'apelle {self.name}{punctuation}'
        return f'Salut {self.customer.name} {m}'
