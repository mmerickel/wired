# request.py
from .models import Greeter, Customer, FrenchCustomer


def process_request(registry):

    # Handle a regular customer by setting the container's context
    # to an instance of Customer
    customer = Customer()
    container = registry.create_container(context=customer)
    greeter = container.get(Greeter)
    greeting = greeter(customer.name)

    # Handle a French customer by making a container with
    # a "context" that is a FrenchCustomer
    french_customer = FrenchCustomer()
    container = registry.create_container(context=french_customer)
    french_greeter = container.get(Greeter)
    french_greeting = french_greeter(french_customer.name)

    return greeting, french_greeting
