# request.py
from models import Greeter, Customer, FrenchCustomer


def process_request(registry):
    # Each request gets its own container
    container = registry.create_container()

    # Handle a regular customer
    customer = Customer()
    greeter = container.get(Greeter)
    greeting = greeter(customer.name)

    # Handle a French customer using "context"
    french_customer = FrenchCustomer()
    french_greeter = container.get(Greeter, context=french_customer)
    french_greeting = french_greeter(french_customer.name)

    return greeting, french_greeting
