# app.py
from dataclasses import dataclass, field

from venusian import Scanner

from wired import ServiceRegistry
from . import models


@dataclass
class App:
    registry: ServiceRegistry = field(default_factory=ServiceRegistry)

    def scan(self):
        # Look for decorators
        scanner = Scanner(registry=self.registry)
        scanner.scan(models)
