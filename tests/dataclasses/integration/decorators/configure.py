from models import Greeter
from wired import ServiceRegistry, ServiceContainer


def greeter_factory(container: ServiceContainer):
    # Some factories might use a container to get other factories
    # that are needed for construction.
    greeter = Greeter()
    return greeter


def register(registry: ServiceRegistry):
    # Wire up the application's registry
    registry.register_factory(greeter_factory, Greeter)
