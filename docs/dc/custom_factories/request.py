# request.py
from wired import ServiceContainer
from .models import Greeter


def process_request(registry, name):
    # Each request gets its own container
    container: ServiceContainer = registry.create_container()

    # Now get the Greeter, which gives the current time
    greeter = container.get(Greeter)
    greeting = greeter()

    return greeting
