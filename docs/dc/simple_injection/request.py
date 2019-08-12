# request.py
from .models import Greeter


def process_request(registry):
    # Each request gets its own container
    container = registry.create_container()

    # Do the work unique to this request and return result
    greeter: Greeter = container.get(Greeter)
    greeting = greeter('Larry')

    return greeting
