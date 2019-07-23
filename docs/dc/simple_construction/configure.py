# configure.py
from wired import ServiceRegistry
from wired.dataclasses import register_dataclass
from .models import Greeter


def register(registry: ServiceRegistry):
    register_dataclass(registry, Greeter)
