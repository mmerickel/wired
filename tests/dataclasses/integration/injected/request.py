# request.py
from models import Greeter, Request


def process_request(registry, name):
    # Each request gets its own container
    container = registry.create_container()

    # Manually make a Request and put in the container
    request = Request(url=name)
    container.set(request, Request)

    # Now get the Greeter, which get Context, which uses the factory
    greeter = container.get(Greeter)
    greeting = greeter()

    return greeting
