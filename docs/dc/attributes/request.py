# request.py
from .models import Greeter, Customer, FrenchCustomer


def process_request(registry):
    # Handle two requests: first a regular Customer and then a
    # FrenchCustomer. In both cases:
    # - Make a request, meaning a container
    # - Make a customer instance matching that request
    # - Stash the customer in the container as the context

    # Handle a regular customer by setting the container's context
    # to an instance of Customer
    regular_customer = Customer(name='Billy')
    container = registry.create_container(context=regular_customer)
    greeter = container.get(Greeter)
    greeting = greeter()

    # Handle a French customer by making a container with
    # a "context" that is a FrenchCustomer
    french_customer = FrenchCustomer(name='Sophie')
    container = registry.create_container(context=french_customer)
    french_greeter = container.get(Greeter)
    french_greeting = french_greeter()

    return greeting, french_greeting
