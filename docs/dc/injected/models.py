
# models.py
from dataclasses import dataclass

from wired.dataclasses import factory, injected


@dataclass
class Request:
    """ The app makes one of these and puts into the container """
    url: str


@dataclass
class Customer:
    """ A basic customer """
    name: str


CUSTOMERS = dict(
    larry=Customer(name='Larry'),
    anne=Customer(name='Anne')
)


@factory()
@dataclass
class Context:
    """ Use request.url to retrieve a customer from the database """

    request: Request

    @classmethod
    def wired_factory(cls, container):
        request = container.get(Request)
        customer = CUSTOMERS.get(request.url)
        return customer


@factory()
@dataclass
class Greeter:
    """ A basic greeter """
    customer: Customer = injected(Context)
    name: str = 'Mary'

    def __call__(self):
        return f'Hello {self.customer.name} my name is {self.name}'
