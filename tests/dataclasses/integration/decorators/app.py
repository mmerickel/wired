import venusian

from wired import ServiceRegistry


def make_registry():
    # Make a registry
    registry = ServiceRegistry()

    # Scan for registrations, in this case, in "models.py"
    scanner = venusian.Scanner(registry=registry)
    import models
    scanner.scan(models)

    # Return the registry
    return registry
