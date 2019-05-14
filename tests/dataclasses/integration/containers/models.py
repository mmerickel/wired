# models.py
from dataclasses import dataclass, field, InitVar

from wired import ServiceContainer
from wired.dataclasses import factory


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
class Greeter:
    """ A basic greeter """
    customer: Customer = field(init=False)
    # TODO Support InitVar...the injector wrongly tries to look
    #   it up instead the generic
    request: InitVar[Request] = None
    container: InitVar[ServiceContainer] = None
    name: str = 'Mary'

    def __post_init__(self, request: Request, container: ServiceContainer):
        request = container.get(Request)
        self.customer = CUSTOMERS.get(request.url)

    def __call__(self):
        return f'Hello {self.customer.name} my name is {self.name}'
