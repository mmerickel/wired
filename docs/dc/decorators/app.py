import venusian

from wired import ServiceRegistry


class App:
    def __init__(self):
        self.registry = ServiceRegistry()
        scanner = venusian.Scanner(registry=self.registry)
        from . import models
        scanner.scan(models)

    def __enter__(self):
        self.container = self.registry.create_container()
        return self.container

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.container:
            del self.container
